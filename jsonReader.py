import json

# 读取原始文件并提取 'answer' 内容
def extract_answers(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            # 创建一个输出文件用于存储整理后的答案
            with open(output_file, 'w', encoding='utf-8') as outfile:
                # 逐行读取文件中的 JSON 内容
                for line in infile:
                    try:
                        # 将每一行解析为 JSON 对象
                        data = json.loads(line.strip())
                        # 如果 JSON 对象中有 "answer" 键，则写入到输出文件
                        if 'answer' in data:
                            # 在每个答案之前加入一个标题说明
                            outfile.write("------ 答案 ------\n")
                            outfile.write(data['answer'] + "\n\n")
                    except KeyError:
                        print("警告：该行没有 'answer' 键，跳过该行。")
                    except json.JSONDecodeError:
                        print("警告：该行无法解析为 JSON 格式，跳过该行。")
                    except Exception as e:
                        print(f"发生未知错误：{e}")
                print(f"答案已成功提取并保存到 {output_file}。")
    except FileNotFoundError:
        print(f"文件 {input_file} 未找到，请检查文件路径是否正确。")
    except Exception as e:
        print(f"发生错误：{e}")

# 调用函数并指定输入输出文件路径
extract_answers('context.txt', 'formatted_answer.md')
