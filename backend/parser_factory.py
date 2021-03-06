import os
import tarfile
from email.parser import Parser
from werkzeug.utils import secure_filename

class FileParser(object):
    def factory(fileType):
        if fileType == "application/x-gzip":
            return TarParser()
        if fileType == "application/octet-stream":
            return MsgParser()

    factory = staticmethod(factory)

class TarParser(FileParser):
    def upload(self, file, upload_folder):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return os.path.join(upload_folder, filename)

    def extract(self, file_path):
        tar = tarfile.open(file_path, "r:gz")
        result = []
        for member in tar.getmembers():
            file = tar.extractfile(member)
            if file is not None:
                content = file.read()
                
                message = Parser().parsestr(content)
                messageId = message['message-id']
                to = message['to']
                sender = message['from']
                subject = message['subject']
                date = message['date']

                message_dictionary = {
                    "msg-id": messageId,
                    "to": to,
                    "sender": sender,
                    "subject": subject,
                    "date": date
                }
                
                result.append(message_dictionary)
        return result

    def parse(self, file, upload_folder): 
        file_path = self.upload(file, upload_folder)
        results = self.extract(file_path)
        return results
        
class MsgParser(Parser):
    def upload(self, file, upload_folder):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return os.path.join(upload_folder, filename)
        
    def extract(self, file_path):     
        file = open(file_path, "r") 
        result = []
        content = file.read()
        
        message = Parser().parsestr(content)
        messageId = message['message-id']
        to = message['to']
        sender = message['from']
        subject = message['subject']
        date = message['date']

        message_dictionary = {
            "msg-id": messageId,
            "to": to,
            "sender": sender,
            "subject": subject,
            "date": date
        }
            
        result.append(message_dictionary)
        file.close()
        
        return result
    
    def parse(self, file, upload_folder): 
        file_path = self.upload(file, upload_folder)
        results = self.extract(file_path)
        return results
        