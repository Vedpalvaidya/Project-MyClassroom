import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import os
import subprocess
import time

class cCompiler(WebsocketConsumer):
    def connect(self):
        self.group_name = 'Compilation'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json['code']
        input_data = text_data_json['input']
        language = text_data_json['language'].strip()
        
        #print("language", language) 
        #print("\n\nHiiiii\n\n")
        #print("code", code,"hello")
        file  = open('submitted_code.txt', 'w')
        file.write(code);
        file.close()
        
        if language == 'c':
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                # {
                #     'type': 'chat_message',
                #     'message': code
                # }

                {
                    'type' : 'compile_c',
                    'code' : code,
                    'input' : input_data
                }
            )
        elif language == 'java':
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type' : 'compile_java',
                    'code' : code,
                    'input' : input_data
                }
            )
        
        elif language == 'c++':
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type' : 'compile_cpp',
                    'code' : code,
                    'input' : input_data
                }
            )

        elif language == 'python':
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type' : 'compile_python',
                    'code' : code,
                    'input' : input_data
                }
            )
            

    def chat_message(self, event):
        message = event['message']
    

        # Send message to WebSocket
        self.send(text_data = json.dumps({
            'message': message
        }))
    
    def compile_c(self, event):
        print("c function called")
        code = event['code']
        input_data = event['input']
        path = os.path.join(os.getcwd(),'compilation/c-compile')
        
        file_path  = os.path.join(path,'input.c')
        input = open(file_path, 'w')
        input.write(code)
        input.close()

        file_path  = os.path.join(path,'input.txt')
        input = open(file_path, 'w')
        input.write(input_data)
        input.close()
        
        

        temp = subprocess.Popen(['bash','compilation/c-compile/compile.sh'],stdout = subprocess.PIPE)
        output = str(temp.communicate())    #allow to continue after completion of previous command

        
        compile_output_path = os.path.join(path,'compile-output.txt')
        output = open(compile_output_path).read()

        print('from compile-output file:')
        print(output)

        if len(output) == 0:
            temp = subprocess.Popen(['bash','compilation/c-compile/run.sh'],stdout = subprocess.PIPE)
            output = str(temp.communicate())

            run_output_path = os.path.join(path,'output.txt')
            output = open(run_output_path).read()

            print('from run file:')
            print(output)

            
        print('from output file:')
        print(output)

        self.send(text_data = json.dumps({
            'code': output
        }))

    def compile_java(self, event):
        print("java function called")
        code = event['code']
        input_data = event['input']
        path = os.path.join(os.getcwd(),'compilation/java')
        
        file_path  = os.path.join(path,'Solution.java')
        input = open(file_path, 'w')
        input.write(code)
        input.close()

        file_path  = os.path.join(path,'input.txt')
        input = open(file_path, 'w')
        input.write(input_data)
        input.close()
        
        

        temp = subprocess.Popen(['bash','compilation/java/compile.sh'],stdout = subprocess.PIPE)
        output = str(temp.communicate())    #allow to continue after completion of previous command

        
        compile_output_path = os.path.join(path,'compile-output.txt')
        output = open(compile_output_path).read()

        print('from compile-output file:')
        print(output)

        if len(output) == 0:
            temp = subprocess.Popen(['bash','compilation/java/run.sh'],stdout = subprocess.PIPE)
            output = str(temp.communicate())

            run_output_path = os.path.join(path,'output.txt')
            output = open(run_output_path).read()

            print('from run file:')
            print(output)

            
        print('from output file:')
        print(output)

        self.send(text_data = json.dumps({
            'code': output
        }))

    def compile_cpp(self, event):
        print("cpp function called")
        code = event['code']
        print("code from cppp")
        print(code)
        input_data = event['input']
        path = os.path.join(os.getcwd(),'compilation/cpp')
        
        file_path  = os.path.join(path,'input.cpp')
        input = open(file_path, 'w')
        input.write(code)
        input.close()

        file_path  = os.path.join(path,'input.txt')
        input = open(file_path, 'w')
        input.write(input_data)
        input.close()
        
        

        temp = subprocess.Popen(['bash','compilation/cpp/compile.sh'],stdout = subprocess.PIPE)
        output = str(temp.communicate())    #allow to continue after completion of previous command

        
        compile_output_path = os.path.join(path,'compile-output.txt')
        output = open(compile_output_path).read()

        print('from compile-output file:')
        print(output)

        if len(output) == 0:
            temp = subprocess.Popen(['bash','compilation/cpp/run.sh'],stdout = subprocess.PIPE)
            output = str(temp.communicate())

            run_output_path = os.path.join(path,'output.txt')
            output = open(run_output_path).read()

            print('from run file:')
            print(output)

            
        print('from output file:')
        print(output)

        self.send(text_data = json.dumps({
            'code': output
        }))

    def compile_python(self, event):
        print("python function called")
        code = event['code']
        input_data = event['input']
        path = os.path.join(os.getcwd(),'compilation/python')
        
        file_path  = os.path.join(path,'input.py')
        input = open(file_path, 'w')
        input.write(code)
        input.close()

        file_path  = os.path.join(path,'input.txt')
        input = open(file_path, 'w')
        input.write(input_data)
        input.close()
        
        

        temp = subprocess.Popen(['bash','compilation/python/compile.sh'],stdout = subprocess.PIPE)
        output = str(temp.communicate())    #allow to continue after completion of previous command

        
        compile_output_path = os.path.join(path,'compile-output.txt')
        output = open(compile_output_path).read()

        print('from compile-output file:')
        print(output)

        if len(output) == 0:
            temp = subprocess.Popen(['bash','compilation/python/run.sh'],stdout = subprocess.PIPE)
            output = str(temp.communicate())

            run_output_path = os.path.join(path,'output.txt')
            output = open(run_output_path).read()

            print('from run file:')
            print(output)

            
        print('from output file:')
        print(output)

        self.send(text_data = json.dumps({
            'code': output
        }))
        




