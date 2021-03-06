import sys, os
sys.path.append('/root/TheMatrix/TheMatrix/TheMatrix')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

'''
product/productId: B00151QYU8
review/userId: AW27MRHR7EQMF
review/profileName: "v_vega"
review/helpfulness: 1/1
review/score: 5.0
review/time: 963014400
review/summary: The best comedy of 1999
review/text: This comedy beats out other great comedies of 1999 like Man On The Moon, and South Park: The Movie. The writer is great, and the direction is cool. The story is one of the best in years. Jason Mewes deserves an award for  his role in this movie (although that is not uncommon for he was great in  Mallrats too!).  Ths film is just great, and in no way does it mean to  insult the Catholic church, i belive that even very religious people can  enjoy this film on its accurate depections of the stories, and its new age  twists. <p>Video God
'''

import re
import Plato.models
#from Plato.models import Review


def parse(fname):
    on = False
    movie_id_N = ""
    user_id_N = ""
    profile_name_N = ""
    helpfulness_N = ""
    score_N = 0 
    time_N = 0 
    summary_N = ""
    full_text_N = ""

    count = 0

    with open(fname) as f:
        for line in f:
            if (count > 5000000):
                break
            if re.match("product/productId: ", line):
#                print('1')
                movie_id_N = re.split("product/productId: ",line)[1]
                movie_id_N = ''.join([i if ord(i) < 128 else ' ' for i in movie_id_N])   
            elif re.match("review/userId: ", line):
 #               print('2') 
                user_id_N = re.split("review/userId: ",line)[1]
                user_id_N = ''.join([i if ord(i) < 128 else ' ' for i in user_id_N])   
            elif re.match("review/profileName: ", line):
  #              print('3') 
                profile_name_N = re.split("review/profileName: ",line)[1]
                profile_name_N = ''.join([i if ord(i) < 128 else ' ' for i in profile_name_N])   
            elif re.match("review/helpfulness: ",line):
   #             print('4')
                helpfulness_N = re.split("review/helpfulness: ",line)[1]
            elif re.match("review/score: ", line):
    #            print('5')
                score_N = re.split("review/score: ",line)[1]
            elif re.match("review/time: ", line):
     #           print('6')
                time_N = re.split("review/time: ",line)[1]
            elif re.match("review/summary: ", line):
      #          print('7')
                summary_N = re.split("review/summary: ",line)[1]
                summary_N = ''.join([i if ord(i) < 128 else ' ' for i in summary_N])   
            elif re.match("review/text: ", line):
       #         print('8')
                full_text_N = re.split("review/text: ",line)[1]
                #full_text_N.decode('ascii', errors='ignore')
                full_text_N = ''.join([i if ord(i) < 128 else ' ' for i in full_text_N])
                #full_text_N = re.sub(r'[^\x00-\x7F]+',' ', full_text_N)
                review = Review.objects.create(
                    movie_id = movie_id_N.strip(), 
                    user_id = user_id_N.strip(), 
                    profile_name = profile_name_N.strip(), 
                    helpfulness = helpfulness_N,
                    score = score_N, 
                    time = time_N, 
                    summary = summary_N.strip(), 
                    full_text = full_text_N.strip())
                review.save()
                count +=1
        #        print review        
            else:
        #        print('ugh')
                continue

if __name__ == "__main__":
    print "HEY DUDE"
    parse('movies.txt')
