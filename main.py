"""
MySQL to SeaTable 数据同步工具
Author: Zhanghui
修改日期：2025-08-05

功能：将MySQL数据库中的数据同步到SeaTable表格中
支持多个数据源和多个同步任务配置

配置项说明：
1. 环境变量配置（.env文件）：
   - MYSQL_HOST: MySQL主机地址
   - MYSQL_PORT: MySQL端口号
   - MYSQL_USER: MySQL用户名
   - MYSQL_PASSWORD: MySQL密码
   - MYSQL_HOST_2: 第二个MySQL主机地址
   - MYSQL_PORT_2: 第二个MySQL端口号
   - MYSQL_USER_2: 第二个MySQL用户名
   - MYSQL_PASSWORD_2: 第二个MySQL密码
   - SEATABLE_SERVER_URL: SeaTable服务器地址

2. 同步任务配置：
   - 合同同步: chpm_v2数据库，合同相关数据
   - 预算同步: projectmng数据库，预算相关数据
   - 外包同步: chpm_v2数据库，外包相关数据
   - 立项研发同步: chpm_v2数据库，研发项目数据
   - 自有软件同步: chpm_v2数据库，软件项目数据
   - 已中未签同步: v9数据库，中标未签约数据
   - 项目进度同步: chpm_v2数据库，项目进度数据
   - 工时数据同步: chpm_v2数据库，工时统计数据
   - OA项目编号同步: v9数据库，OA项目编号数据
   - OA立项编号同步: v9数据库，OA立项编号数据
   - OA销售团队同步: v9数据库，销售团队数据
   - 回款信息同步: projectmng数据库，回款相关数据

3. 配置文件说明：
   - 每个同步任务对应一个JSON配置文件
   - 配置文件包含SeaTable映射、数据映射、SQL查询等
   - 支持数据合并规则和字段映射转换

4. 程序特性：
   - 支持循环菜单，可连续执行多个同步任务
   - 自动清空目标表格后插入新数据
   - 支持大数据量分批处理
   - 错误处理和重试机制
   - 支持Decimal和日期格式转换
"""

import json
import pymysql
from seatable_api import Base
from dotenv import load_dotenv
import os
import sys
from decimal import Decimal
import datetime

# 加载 .env 文件中的环境变量
load_dotenv()

# 从 .env 文件中读取基本配置（不包括数据库和API令牌）
mysql_config_1 = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
}

mysql_config_2 = {
    'host': os.getenv('MYSQL_HOST_2'),
    'port': int(os.getenv('MYSQL_PORT_2')),
    'user': os.getenv('MYSQL_USER_2'),
    'password': os.getenv('MYSQL_PASSWORD_2'),
}

seatable_config = {
    'server_url': os.getenv('SEATABLE_SERVER_URL'),
}

# 全局变量，将在用户选择后设置
seatable_mappings = None
data_mappings = None
chunk_size = None
current_mysql_config = None

# 获取并打印基础库的元数据
def get_metadata(base):
    metadata = base.get_metadata()
    print("Metadata retrieved from SeaTable:")
    print(metadata)

# 函数：清空Seatable表格
def clear_table(base, chunk_size=100):
    """通过循环删除清空 Seatable 表，处理分页限制"""
    table_name = seatable_mappings['table_name']
    total_deleted = 0
    
    print(f"Starting to clear table '{table_name}'...")
    
    # 循环删除直到表为空
    while True:
        # 每次都重新获取行（处理分页限制）
        rows = base.list_rows(table_name)
        if not rows:
            print(f"Table '{table_name}' is now empty. Total deleted: {total_deleted} rows")
            return True
            
        current_batch_size = len(rows)
        print(f"Found {current_batch_size} rows in current batch...")
        
        # 针对删除操作优化批次大小
        if current_batch_size > 500:
            delete_chunk_size = min(chunk_size, 200)  # 大批次时适度减小chunk
        else:
            delete_chunk_size = min(chunk_size, 100)  # 小批次时保持稳定
            
        row_ids = [row['_id'] for row in rows]
        deleted_in_this_round = 0
        failed_deletes = []
        
        # 批量删除当前获取的行
        for i in range(0, len(row_ids), delete_chunk_size):
            chunk = row_ids[i:i + delete_chunk_size]
            try:
                base.batch_delete_rows(table_name, chunk)
                deleted_in_this_round += len(chunk)
                total_deleted += len(chunk)
            except Exception as e:
                print(f"Error in batch delete: {e}")
                # 如果批量删除失败，尝试逐个删除这个chunk
                for row_id in chunk:
                    try:
                        base.delete_row(table_name, row_id)
                        deleted_in_this_round += 1
                        total_deleted += 1
                    except Exception as e2:
                        print(f"Failed to delete row {row_id}: {e2}")
                        failed_deletes.append(row_id)
        
        print(f"Deleted {deleted_in_this_round} rows in this round. Total: {total_deleted}")
        
        # 如果这一轮没有成功删除任何行，说明遇到了问题
        if deleted_in_this_round == 0:
            print(f"No rows were deleted in this round. There may be permission issues or other errors.")
            remaining_rows = base.list_rows(table_name)
            if remaining_rows:
                print(f"ERROR: Unable to completely clear table '{table_name}'. {len(remaining_rows)} rows remain.")
                return False
            else:
                return True
                
        # 如果删除的行数少于当前批次大小，可能还有更多数据，继续循环
        if deleted_in_this_round < current_batch_size and failed_deletes:
            print(f"Some deletions failed. {len(failed_deletes)} rows could not be deleted.")
    
    return True

# 函数：执行SQL查询
def execute_sql_query(connection, sql_query):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql_query)
        return cursor.fetchall()

# 函数：基于映射处理数据
def process_data_based_on_mapping(data, field_mappings):
    processed_data = []
    for item in data:
        row_data = {}
        for mysql_field, seatable_field in field_mappings.items():
            value = item[mysql_field]
            
            # 处理 Decimal 类型（金额）
            if isinstance(value, Decimal):
                # 转换为带千分位的字符串格式
                value = f"{value:,.2f}"
            
            # 处理日期格式
            elif isinstance(value, (datetime.date, datetime.datetime)):
                value = value.strftime('%Y-%m-%d')
            
            row_data[seatable_field] = value
        processed_data.append(row_data)
    return processed_data

# 函数：将数据分批插入到Seatable
def insert_data_into_seatable(base, data, table_name, chunk_size):
    for chunk in chunked_data(data, chunk_size):
        base.batch_append_rows(table_name, chunk)

# 函数：分批处理数据
def chunked_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# 函数：将数据单行插入到Seatable
def insert_singledata_into_seatable(base, data, table_name):
    for row in data:
        base.append_row(table_name, row)

# 函数：应用合并规则
def apply_merge_rules(main_data, additional_data, merge_rules):
    on_field = merge_rules["on"]
    target_field = merge_rules["target_field"]

    # 创建一个基于on_field的查找字典，用于快速找到main_data中的对应行
    main_data_lookup = {item[on_field]: item for item in main_data}

    # 遍历附加数据，根据合并规则更新主数据集
    for item in additional_data:
        key = item[on_field]
        if key in main_data_lookup:
            # 如果找到匹配的行，更新target_field
            main_data_lookup[key][target_field] = item[target_field]


# 函数：主同步
def sync_mysql():
    """Sync database into the table
    """
    # 连接到MySQL数据库
    connection = pymysql.connect(**current_mysql_config)
    
    # 连接到SeaTable
    base = Base(seatable_config['api_token'], seatable_config['server_url'])
    base.auth()
    #base.use_api_gateway=False
    #get_metadata(base)

    # Clear table
    if not clear_table(base, chunk_size):
        print("Failed to completely clear the table. Aborting sync operation.")
        return

    main_data = []
    additional_data = {}

    try:
        for mapping in data_mappings:
            data = execute_sql_query(connection, " ".join(mapping["sql_query"]))
            processed_data = process_data_based_on_mapping(data, mapping["field_mappings"])

            if "merge_rules" in mapping:
                # 如果有合并规则，暂存处理过的数据用于后续合并
                additional_data[mapping["description"]] = processed_data
            else:
                # 存储主数据集
                main_data = processed_data

        # 如果存在需要合并的数据
        if additional_data:
            for description, data in additional_data.items():
                merge_rules = next(filter(lambda m: m.get("description") == description, data_mappings), {}).get("merge_rules", {})
                apply_merge_rules(main_data, data, merge_rules)

        # 插入到Seatable
        #print("main_data:", main_data)
        insert_data_into_seatable(base, main_data, seatable_mappings['table_name'], chunk_size)
        #insert_singledata_into_seatable(base, main_data, seatable_mappings['table_name'])

    finally:
        connection.close()

def select_configuration():
    print("\n===== 同步任务选择 =====")
    
    # 从环境变量获取SeaTable API tokens
    def get_token(token_name):
        token = os.getenv(token_name)
        if not token:
            print(f"错误: 未找到环境变量 {token_name}")
            print("请检查 .env 文件是否正确配置")
            return None
        return token

    # 整合数据库和SeaTable表的选项
    config_options = {
        1: {
            "name": "合同同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_CONTRACT"),
            "config_file": "memo-contract.json",
            "mysql_config": mysql_config_1
        },
        2: {
            "name": "自有软件同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_OS"),
            "config_file": "memo-os.json",
            "mysql_config": mysql_config_1
        },
        3: {
            "name": "项目进度同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_PROGRESS"),
            "config_file": "memo-progress.json",
            "mysql_config": mysql_config_1
        },
        4: {
            "name": "预算同步",
            "db": "projectmng",
            "token": get_token("SEATABLE_TOKEN_PURCHASE"),
            "config_file": "memo-purchase.json",
            "mysql_config": mysql_config_1
        },
        5: {
            "name": "工时数据同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_WORKTIME"),
            "config_file": "memo-worktime.json",
            "mysql_config": mysql_config_1
        },
        6: {
            "name": "回款信息同步",
            "db": "projectmng",
            "token": get_token("SEATABLE_TOKEN_PAYIN"),
            "config_file": "memo-payin.json",
            "mysql_config": mysql_config_1
        },
        7: {
            "name": "OA项目编号同步",
            "db": "v9",
            "token": get_token("SEATABLE_TOKEN_PROJECT"),
            "config_file": "memo-project.json",
            "mysql_config": mysql_config_2
        },
        8: {
            "name": "OA立项编号同步",
            "db": "v9",
            "token": get_token("SEATABLE_TOKEN_PI"),
            "config_file": "memo-pi.json",
            "mysql_config": mysql_config_2
        },
        9: {
            "name": "OA销售团队同步",
            "db": "v9",
            "token": get_token("SEATABLE_TOKEN_GSSALES"),
            "config_file": "memo-gssales.json",
            "mysql_config": mysql_config_2
        },
        10: {
            "name": "已中未签同步",
            "db": "v9",
            "token": get_token("SEATABLE_TOKEN_YZWQ"),
            "config_file": "memo-yzwq.json",
            "mysql_config": mysql_config_2
        },
        11: {
            "name": "立项研发同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_RD"),
            "config_file": "memo-rd.json",
            "mysql_config": mysql_config_1
        },
        12: {
            "name": "外包同步",
            "db": "chpm_v2",
            "token": get_token("SEATABLE_TOKEN_OUTSOURCE"),
            "config_file": "memo-outsource.json",
            "mysql_config": mysql_config_1
        },
        0: {
            "name": "退出程序",
            "action": "exit"
        }
    }
    
    # 显示选项
    for key, value in config_options.items():
        if key == 0:
            print(f"{key}. {value['name']}")
        else:
            print(f"{key}. {value['name']}")
    
    # 获取用户选择
    while True:
        try:
            choice = int(input("\n请选择要执行的同步任务 (0-12): "))
            if 0 <= choice <= 12:
                break
            else:
                print("无效选择，请输入0-12之间的数字")
        except ValueError:
            print("请输入有效的数字")
    
    selected_config = config_options[choice]
    
    # 检查是否为退出选项
    if choice == 0:
        print("\n感谢使用！再见！")
        sys.exit(0)
    
    # 验证token是否有效
    if not selected_config["token"]:
        print(f"\n错误: {selected_config['name']} 的API Token未配置")
        print("请检查 .env 文件中的配置，然后重试")
        return None
    
    # 设置环境变量
    os.environ["MYSQL_DB"] = selected_config["db"]
    os.environ["SEATABLE_API_TOKEN"] = selected_config["token"]
    
    # 更新配置字典
    global current_mysql_config
    current_mysql_config = selected_config["mysql_config"]
    current_mysql_config['db'] = selected_config["db"]
    seatable_config['api_token'] = selected_config["token"]
    
    print(f"\n已选择: {selected_config['name']}")
    print(f"数据库: {selected_config['db']}")
    print(f"配置文件: {selected_config['config_file']}")
    
    return selected_config

# 修改主函数
if __name__ == '__main__':
    while True:
        try:
            # 选择配置
            selected_config = select_configuration()
            
            # 加载选定的配置文件
            with open(selected_config['config_file'], 'r') as f:
                config = json.load(f)
            
            # 设置全局变量
            seatable_mappings = config['seatable']
            data_mappings = config['data_mappings']
            chunk_size = config['chunk_size']
            
            # 执行同步
            print(f"\n开始执行 {selected_config['name']} 同步...")
            sync_mysql()
            print(f"\n{selected_config['name']} 同步完成！")
            print("\n" + "="*50)
                    
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见！")
            sys.exit(0)
        except Exception as e:
            print(f"\n执行过程中出现错误: {e}")
            retry = input("是否重试？(y/n): ").lower().strip()
            if retry not in ['y', 'yes', '是']:
                print("程序退出")
                sys.exit(1)
