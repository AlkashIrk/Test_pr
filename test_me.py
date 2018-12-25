import sys
import argparse
import re
from InstagramAPI import InstagramAPI
from rrr import FileOperations


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    parser.add_argument('-p', '--passw')
    parser.add_argument('-t', '--task', default='run')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    USER=namespace.name
    PASSWORD=namespace.passw
    TASK=namespace.task
    file_op=FileOperations()
    count=0
    old_count=-1
    count_total=1
    count_pause=50
    pause_min=30
    pause_max=50
    time_to_sleep=30
    time_to_sleep=60*time_to_sleep


def not_arabian(data_from_insta):
    strings_list = [r'[\u0600-\u06ff]', 'shop', 'магазин','продвижен','реклам', 'для','заказ', 'сайт']
    for strings in strings_list:
        token=data_from_insta.split(';')
        not_arab=True
        for w in token:
            status=re.search(strings,w.lower())
            if status:
                not_arab=False
                return not_arab
                break
    return not_arab

api = InstagramAPI(USER, PASSWORD)
api.login()
# list_dict=file_op.read_from_file('\\lists\\tag_.txt')

e=api.info_user('8099166791')

print(e['user']['follower_count'] + ' follower')
print(e['user']['following_count']+ ' following')



exit()

for list in list_dict:
    user_id_dict=api.testplease(list)
    if user_id_dict['num_results']>=1:
        user_id_dict=user_id_dict['users']
        user_id=user_id_dict[0]['pk']
        for item in user_id_dict:
            item_username=item['username']
            if item_username==list.lower().rstrip():
                user_id=item['pk']
                # a=api.getTotalSelfFollowers(user_id)
                # b=api.getTotalSelfFollowings(user_id)
                following_status=item['friendship_status']['following']
                test=str(item['username']) +';' + str(item['full_name'])
                print(list.rstrip())
                print(test)
                print(not_arabian(test))
                print(" ")
                print(" ")


exit()


#
#


#
# print(os.path.isfile(path_full + 'log.log'))
#
#
#
# print(cwd)


exit()



test=read_from_file('lists/unfollow_list_psycho_growth.txt')
test2=read_from_file('lists/111.txt')
#
#
unfollow_list=list(set(test2)-set(test))




for line_f in unfollow_list:
    # token=line_f.split(';')
    # token_str=str(token[2]).rstrip()
    # print(token_str)
    print(line_f.rstrip())


aaaa=90

test=read_from_file('lists/followings_psycho_growth.txt_')
test=read_from_file('lists/followings_psycho_growth.txt_')
# test=u"working جنگ test  بندی کروانا not good"




strings = [r'[\u0600-\u06ff]', 'shop', 'магазин','продвижен','реклам', 'для','заказ', 'сайт']

for strings_ex in strings:
    for line_f in test:
        token=line_f.split(';')
        ttt=False
        for w in token:
            status=re.search(strings_ex,w.lower())
            if status:
                ttt=True
                # print(w)
                break
        if ttt:
            print(line_f.rstrip())
        #







# path_full=os.path.dirname(os.path.realpath(__file__)) + '/'
#
# print(os.path.isfile(path_full + 'log.log'))
# print(path_full)
#
#
# b=50//7
#
# print(b)

# write_to_file('test','log\logd.log')

