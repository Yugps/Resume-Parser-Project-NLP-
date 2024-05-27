
# First Install pyngrok using !pip install pyngrok

from transformers import pipeline
pipe=pipeline(task='ner',model='resume_ner_model_saved',tokenizer='Bert_tokenizer')


from flask import Flask,render_template,request
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re

 
from pyngrok import ngrok
port_no=5000


app = Flask(__name__)
port_no = 5000  # Define the port number

ngrok.set_auth_token('2dW7qeQXYf1RbmtHWu1mUriKQnC_6qjCtetiLtbfKXVY6R1ZZ')
public_url = ngrok.connect(port_no).public_url

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def main_function():
    if request.method == 'POST':
        try:
            resume = str(request.form.get('content'))

            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,64}'
            extracted_emails = re.findall(email_pattern, resume)
            resume=resume.replace(extracted_emails[0],'')



            url_pattern =  r'(https?://(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+/?[^\s]*)'
            extracted_links = re.findall(url_pattern, resume)
            for i in extracted_links:
              resume=resume.replace(i,'')


            phone_pattern = r"(?:(?:\+91)?[6789]\d{9})"
            phone_numbers=re.findall(phone_pattern, resume)
            resume=resume.replace(phone_numbers[0],'')



            predictions =pipe(resume)

            all_stop_words = stopwords.words('english')
            punctuations=[',','.','-','/']


            for prediction in predictions:

              if prediction['word'] in all_stop_words or prediction['word'] in punctuations or prediction['score'] <= 0.35 or prediction['entity'] == 'Email Address':
                    prediction['entity'] = 'Irrelevant Info'
              else:
                pass


            indexes=[]
            for i in range(0,len(predictions)):
              sub=predictions[i]
              if sub['entity']!='Irrelevant Info':
                indexes.append(i)
            filtered_results=[]
            for i in indexes:
              filtered_results.append(predictions[i])



            hash_tag_indexes=[]
            for i in range(0,len(filtered_results)):
              if filtered_results[i]['word'][0]=='#':
                j=i
                while filtered_results[j]['word'][0]=='#':
                  j=j-1

                filtered_results[j]['word']=filtered_results[j]['word']+filtered_results[i]['word'][2:]
              else:
                hash_tag_indexes.append(i)


            final_filtered_results=[]
            for i in hash_tag_indexes:
              final_filtered_results.append(filtered_results[i])


            parsed_resume = []
            parsed_resume.append({'word': extracted_emails[0], 'entity': 'Email Address' })
            parsed_resume.append({'word': phone_numbers[0], 'entity': 'Phone Number' })

            for i in extracted_links:
              parsed_resume.append({'word': i, 'entity': 'Profile Url' })

            for prediction in final_filtered_results:
              word = prediction['word']
              entity = prediction['entity']
              if entity=='Irrelevant Info':
                pass
              else:
                parsed_resume.append({'word': word, 'entity': entity})




            return render_template('result.html', parsed_resume=parsed_resume)
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    print(f'To access the global link please click {public_url}')
    app.run(port=port_no)

