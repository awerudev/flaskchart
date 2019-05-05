from flask import Flask, render_template, request
#from nocache import nocache
import ast, requests, boto3, os
from datetime import datetime
import csv
# import plots,copy,random,string
# access_key_id = 'ASIA37PBWIRNEDGEMZO2'
# secret_access_key = "+QT0v4mCGOxm7"
# session_token = '+dP/EIgDIcZgOUcuzlLHRY9glf+/SYI6CBvnEYPOtumiuqdCgHJZLUrYjZx0AsENG9BMgodHcFk8u/cSppfhzjYwWbGKzyBuNiWvpQrpNwVrpO+O+J3ORApG0/jnIv8ibN8oxqLa4QU='
#
app = Flask(__name__)
# app.config['SECRET_KEY'] = '0f9dc56d2288afa6e1'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#
#
# types = {"Government" : 0, "Education" : 0, "Invalid URL" : 0, "Social Media" : 0,
#   "News" : 0, "Blog" : 0, "Commercial Health" : 0, "Fake News" : 0, "Scientific" : 0,
#   "Videos" : 0, "Commercial" : 0, "HealthMagazines" : 0, "HealthInsurance" : 0,
#   "NMPSocieties" : 0, "None Found" : 0}
#
# table_dict = {"vaccine" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "abortion" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "weed" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "ecig" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "aids" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types))}
#
region = 'us-east-2'
# session = boto3.session.Session()
aws_secret = 'aXL3ndaT/BilMryekS'
aws_pub = 'AKIAIFL3OJZQZDFSJOQQ'
db = boto3.resource('dynamodb',aws_access_key_id=aws_pub,aws_secret_access_key=aws_secret, region_name=region)
# img_folder = '/home/trevorm4/mysite/static/img/'

# No caching at all for API endpoints.
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response
#
# """
# Uses Twitter oEmbed api to fetch the html code for embedding the tweet.
# Uses fix_twitter_html_response because the api escapes '/', even though its not necessary,which
# messes up the code
#
# @param tweet_url : url of the tweet to fetch html code for
# @return html code to embed passed tweet
# """
# def get_embed_html(tweet_url):
#   r = requests.get('https://publish.twitter.com/oembed?url='+tweet_url)
#   r = fix_malformed_dict_string(r.text)
#   return fix_twitter_html_response((ast.literal_eval(r)['html']))
#
# def fix_twitter_html_response(html):
#   new_string = ""
#   for i in range(len(html)):
#     if not (html[i] == "\\" and html[i:i+2] == '\\/'):
#       new_string += html[i]
#   return new_string
#
# """
# Some of the JSONs have false/true/null instead of False/True/None
# So this method just replaces all of false/true/null with False/True/None so ast.literal_eval can
# parse it extremely easily
# """
# def fix_malformed_dict_string(dict_string):
#   no_null = dict_string.replace('null','None')
#   no_false = no_null.replace('false','False')
#   no_true = no_false.replace('true','True')
#   return no_true
#
# def get_latest_tweets(table_name,num_tweets,topic):
#   table = db.Table(table_name)
#   response = table.scan()
#   tweets = []
#
#   for item in response['Items']:
#     if item['topic'] == topic.lower():
#         tweets.append(get_embed_html(item['TweetID']))
#   return tweets[:num_tweets]
#
# def update_counts(table_name,dictionary):
#   table = db.Table(table_name)
#
#   response = table.scan()
#
#   for item in response["Items"]:
#     category = item['topic']
#     url_type = item['type']
#     dictionary[category][0][url_type] += 1 #overall count
#     if item['user_type'] == 'Bot':
#       dictionary[category][2][url_type] += 1
#     else:
#       dictionary[category][1][url_type] += 1
#
# def update_plots(category):
#   update_counts('URLsTable',table_dict)
#   cat = category
#   plots.type_histogram_overall(table_dict[cat][0],True, category + '_PLOT_'+ generate_random_string(10) + '.png')
#   plots.type_histogram_overall(table_dict[cat][2],True, category + '_PLOT_'+ generate_random_string(10) + '_human_' +'.png')
#   plots.type_histogram_overall(table_dict[cat][2],True, category + '_PLOT_'+ generate_random_string(10) + '_bot_'+ '.png')
#
# def generate_random_string(n):
#   return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
#
# def get_plot_html(category):
#   existing_files = [file for file in os.listdir(img_folder) if file.find(category + '_PLOT_') == 0]
#
#   for file in existing_files:
#     os.remove(os.path.join(img_folder,file))
#   update_plots(category)
#
#   files = os.listdir(img_folder)
#   files = [file for file in files if file.find(category + '_PLOT_') == 0]
#   html_blocks = []
#
#   for file in files:
#     print('<img src=\"' + img_folder + file + '\" alt=\"' + file[:file.find('.png')] + '\">')
#     html_blocks.append('<img src=\"' + '/static/img/' + file + '\" alt=\"' + file[:file.find('.png')] + '\">')
#   return html_blocks


#app route

@app.route('/', methods=['POST', 'GET'])
def dash():


    # with open('AllTweet.csv', encoding="utf8") as f:
    #     rd = csv.reader(f)
    #     for row in rd:
    #         data_list.append(row)

    # Get the full table
    table = db.Table('AllTweet')
    # With Scan get the full table data
    data = table.scan()
    # get the first item
    data_One = data['Items']

    # initialize the varialbe outside of loop to avoid error when the app loads without any result or first time when the app loads, there will be no result
    result_list = []
    positive = 0
    negative = 0
    neutral =0

    # get the search topic
    search_topic = ''
    if request.method == 'POST':
        search_topic = request.form['topic']

    for item in data_One:
        if item['topic'] == search_topic:
            result_list.append(item)
    # ===================================================
    # calculate the neautral, negative, positive number
    # ================================================
    for item in result_list:
        if item['sentiment'] == "Neutral":
            neutral += 1
        if item['sentiment'] == "Negative":
            negative += 1
        if item['sentiment'] == "Positive":
            positive += 1




    # ==================================================
    # calculate the number of topic happended each day
    # ===============================================
    all_day_list = []
    unique_day_list = []
    for item in result_list:
        all_day_list.append(item['created_at'].split()[0].split('-')[-1])
    for item in all_day_list:
        if item not in unique_day_list:
            unique_day_list.append(item)

    each_day_topic_list = []
    day_first = 0
    day_second = 0
    for item in result_list:
        if item['created_at'].split()[0].split('-')[-1] == unique_day_list[0]:
            day_first += 1

    if day_first != len(result_list):
        day_second = len(result_list) - day_first


    # ================================================================================
    # getting url support number for each search topic from URLsTable table from aws
    # =============================================================================
    # Get the full table
    url_table = db.Table('URLsTable')
    # With Scan get the full table data
    url_data = url_table.scan()
    # get the first item
    url_data_One = data['Items']

    total_url_for_search_topic = []
    url_supported_link = 0
    url_non_supported_link = 0

    # getting all urls for search topic
    for item in url_data_One:
        if item['topic'] == search_topic:
            for key, val in item.items():
                try:
                    if "/" in val:
                        total_url_for_search_topic.append(val)
                except:
                    pass

    # getting total url number which contain the serach topic word
    for item in total_url_for_search_topic:
        if search_topic in item:
            url_supported_link += 1

    # getting non_supported_url number
    url_non_supported_link = len(total_url_for_search_topic) - url_supported_link


    # =================================================
    # Calculating total unique account for each topic
    # ==============================================
    all_account_list = []
    unique_account_list = []
    total_account = 0
    topics_per_account = 0
    for item in result_list:
        all_account_list.append(item['username'])
    for item in all_account_list:
        if item not in unique_account_list:
            unique_account_list.append(item)
    total_account = len(unique_account_list)
    if result_list:
        topics_per_account = round((len(result_list) / total_account), 2)



    # ==============================================
    # Calculating total BOT account for each topic
    # ===========================================
    total_bot_account = 0
    for item in result_list:
        if item['user_type'] == 'Bot':
            total_bot_account += 1



    # ==============================================
    # Calculating % of true account for each topic
    # ===========================================
    true_account_percentage_full_decimal = 0
    true_account_percentage = 0
    if result_list:
        true_account_percentage_full_decimal = 100 - ((total_bot_account * 100) / len(result_list))
        true_account_percentage = round(true_account_percentage_full_decimal, 2)



    # ===============================================================
    # Calculating url & non-url for each sentiment for Search topic
    # ===========================================================
    negative_result_list = []
    positive_result_list = []
    neutral_result_list = []
    if result_list:
        for item in result_list:
            if item['sentiment'] == "Negative":
                negative_result_list.append(item['TweetID'])
            if item['sentiment'] == "Positive":
                positive_result_list.append(item['TweetID'])
            if item['sentiment'] == "Neutral":
                neutral_result_list.append(item['TweetID'])
    negative_url_result_list = []
    positive_url_result_list = []
    neutral_url_result_list = []

    negative_with_url = 0
    negative_with_out_url = 0
    positive_with_url = 0
    positive_with_out_url = 0
    neutral_with_url = 0
    neutral_with_out_url = 0



    for item in negative_result_list:
        for id in url_data_One:
            if item == id['TweetID']:
                negative_url_result_list.append(id)

    for item in positive_result_list:
        for id in url_data_One:
            if item == id['TweetID']:
                positive_url_result_list.append(id)

    for item in neutral_result_list:
        for id in url_data_One:
            if item == id['TweetID']:
                neutral_url_result_list.append(id)

    if search_topic:
        for item in negative_url_result_list:
            for key, val in item.items():
                try:
                    if "/" in val:
                        if search_topic in val:
                            negative_with_url += 1
                except:
                    pass
        negative_with_out_url = len(negative_url_result_list) - negative_with_url

        for item in positive_url_result_list:
            for key, val in item.items():
                try:
                    if "/" in val:
                        if search_topic in val:
                            positive_with_url += 1
                except:
                    pass
        positive_with_out_url = len(positive_url_result_list) - positive_with_url

        for item in neutral_url_result_list:
            for key, val in item.items():
                try:
                    if "/" in val:
                        if search_topic in val:
                            neutral_with_url += 1
                except:
                    pass
        neutral_with_out_url = len(neutral_url_result_list) - neutral_with_url


    return render_template('dashboard.html', result_list=result_list, positive=positive, negative=negative, neutral=neutral, search_topic=search_topic, unique_day_list=unique_day_list, url_supported_link=url_supported_link, url_non_supported_link=url_non_supported_link, day_first=day_first, day_second=day_second, total_account=total_account, topics_per_account=topics_per_account, total_bot_account=total_bot_account, true_account_percentage=true_account_percentage, negative_with_url=negative_with_url, negative_with_out_url=negative_with_out_url, positive_with_url=positive_with_url, positive_with_out_url=positive_with_out_url, neutral_with_url=neutral_with_url, neutral_with_out_url=neutral_with_out_url)






@app.route('/analyze')
def analyze():
    return render_template('dashboard.html',tweets=get_latest_tweets('AllTweet',15,'aids'))


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/graph/')
def graph():

    # table = db.Table('AllTweet')
    # tabdata = table.creation_date_time
    # # num_of_item = table.item_count
    # data = table.scan()
    # data_One = data['Items']
    # result_list = []
    # topic_list = []
    # unique_topic_list = []
    # created_at_column_data = []
    #
    #
    # for item in data_One:
    #     # if item['topic'] == 'weed':
    #     #     result_list.append(item)
    #     topic_list.append(item['topic'])
    #     created_at_column_data.append(item['created_at'])
    #
    # # getting the unique topic list
    # for item in topic_list:
    #     if item not in unique_topic_list:
    #         unique_topic_list.append(item)

    table = db.Table('URLsTable')
    data = table.scan()
    data_One = data['Items']

    # num_of_item = len(result_list)
    return render_template('graph.html', data_One=data_One)



#
# @app.route('/vaccines')
# def vaccines():
#   #tweetss = get_latest_tweets('tweets_by_ID',15)
#   graphs = get_plot_html("vaccine")
#   return render_template('vaccines.html',charts=graphs)
#
# @app.route('/abortion')
# def abortion():
#     #tweetss = get_latest_tweets('abortion_tweets_by_ID',15)
#     graphs = get_plot_html("abortion")
#     return render_template('abortion.html',charts=graphs)
# @app.route('/marijuana')
# def weed():
#     #tweetss = get_latest_tweets('weed_tweets_by_ID',15)
#     graphs = get_plot_html('weed')
#     return render_template('weed.html', charts = graphs)
# @app.route('/aids')
# def aids():
#     #tweetss = get_latest_tweets('aids_tweets_by_ID',15)
#     graphs = get_plot_html('aids')
#     return render_template('aids.html', charts = graphs)
# @app.route('/ecigs')
# def ecigs():
#     #tweetss = get_latest_tweets('ecig_tweets_by_ID',15)
#     graphs = get_plot_html('ecig')
#     return render_template('ecigs.html', charts = graphs)


if __name__ == "__main__":
    app.run(debug=True)
