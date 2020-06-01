import os

def remove_files(n):
    for file in os.listdir(data_dir):
        name, ext = os.path.splitext(file)
        if int(name) >= n:
            full_path = os.path.join(data_dir, file)
            os.remove(full_path)
            
            
if __name__ == '__main__':
    for model in os.listdir('models'):
        print(model)
        data_dir = os.path.join('post_processing', 'rouge_score', model)
        remove_files(1000)
