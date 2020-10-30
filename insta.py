import sys
import argparse
import time
import random
import re
import datetime
from InstagramAPI import InstagramAPI
from rrr import FileOperations



def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str)
    parser.add_argument('-p', '--passw', type=str)
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


def getfollowers(user_name):

    user_name=str(user_name).lower().rstrip()
    api = InstagramAPI(USER, PASSWORD)
    api.login()
    user_id_dict=api.testplease(user_name)
    user_id_dict=user_id_dict['users']
    user_id=user_id_dict[0]['pk']
    for item in user_id_dict:
        item_username=item['username']
        item_username=str(item_username).lower().rstrip()
        if item_username==user_name:
            user_id=item['pk']
            break

    if user_name==str(USER).lower().rstrip():
        followers = api.getTotalFollowers(user_id)
        followers_file_path='\\lists\\followers_' + user_name
        followings = api.getTotalFollowings(user_id)
        followings_file_path='\\lists\\followings_' + user_name

        file_op.remove_file(followers_file_path + '.txt')
        file_op.remove_file(followers_file_path + '_full.txt')
        file_op.remove_file(followings_file_path + '.txt')
        file_op.remove_file(followings_file_path + '_full.txt')

        element=[]
        full_data=[]
        for item in followers:
            element.append(item['username'])
            full_data.append(str(item['pk']) + ";" + str(item['username']) + ";" + str(item['full_name']))
        file_op.write_to_file(element, followers_file_path + '.txt')
        file_op.write_to_file(full_data, followers_file_path + '_full.txt', 1)

        element=[]
        full_data=[]
        for item in followings:
            element.append(item['username'])
            full_data.append(str(item['pk']) + ";" + str(item['username']) + ";" + str(item['full_name']))
        file_op.write_to_file(element, followings_file_path + '.txt')
        file_op.write_to_file(full_data, followings_file_path + '_full.txt' ,1)

        unfollowlist()
    else:
        element=[]
        followers = api.getTotalFollowers(user_id)
        followers_file_path='\\lists\\tag.txt'
        file_op.remove_file(followers_file_path)
        for item in followers:
            element.append(item['username'])
            # full_data.append(str(item['pk']) + ";" + str(item['username']) + ";" + str(item['full_name']))
        file_op.write_to_file(element, followers_file_path)
        # file_op.write_to_file(full_data, followers_file_path + '_full.txt', 1)

    return

def unfollowlist():
    followings=file_op.read_from_file('\\lists\\followings_' + USER + '.txt')
    followers=file_op.read_from_file('\\lists\\followers_' + USER + '.txt')
    unfollow_list=list(set(followings)-set(followers))

    file_op.remove_file('\\lists\\unfollow_list_' + USER + '.txt')
    file_op.write_to_file(unfollow_list, '\\lists\\unfollow_list_' + USER + '.txt')


if TASK=='run':
    if file_op.file_exist('\\lists\\followers_' + USER +'.txt')==False:
        getfollowers(USER)

    completed=file_op.read_from_file('\\lists\\black_list.txt')      #
    followers=file_op.read_from_file('\\lists\\followers_' + USER +'.txt')       #
    follow=file_op.read_from_file('\\lists\\tag.txt')                #
    follow_list=list(set(follow)-set(completed)-set(followers))

    completed.clear()
    followers.clear()
    follow.clear()

    if len(follow_list)>=1:
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file('------------------------------', '\\log.log')
        file_op.write_to_file('------------------------------', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')

        print(str(len(follow_list)) + ' positions in follow list')
        file_op.write_to_file(str(len(follow_list))  + ' positions in follow list','\\log.log')

        api = InstagramAPI(USER, PASSWORD)
        api.login()

        user_id_dict=api.testplease(USER)
        if user_id_dict['num_results']>=1:
            user_id_dict=user_id_dict['users']
            user_id=user_id_dict[0]['pk']
            for item in user_id_dict:
                item_username=item['username']
                if item_username==USER.lower():
                    user_id=str(item['pk'])
                    user_data_dict=api.info_user(user_id)
                    data_str=str(str(user_data_dict['user']['follower_count']) + ' followers' + '  ' + str(user_data_dict['user']['following_count'])+ ' following')
                    print(data_str)
                    file_op.write_to_file(data_str,'\\log.log')


        for list in follow_list:
            list=str(list).rstrip()
            if count_total>=500:
                print('Complete!!!')
                file_op.write_to_file("Complete!!!", '\\log.log')
                # file_op.remove_file(unfollow_list_path)
                api.logout()
                break
            user_id_dict=api.testplease(list)

            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            if user_id_dict['num_results']>=1:
                user_id_dict=user_id_dict['users']
                user_id=user_id_dict[0]['pk']
                for item in user_id_dict:
                    item_username=item['username']
                    if item_username==list.lower():
                        user_id=item['pk']
                        following_status=item['friendship_status']['following']
                        test=str(item['username']) +';' + str(item['full_name'])

                        not_arab=not_arabian(test)
                        if not_arab==False:
                            print('Arab_detected!!! ' + test)
                        break
                if following_status==False and not_arab==True:
                    api.follow(user_id)
                    print(st + " " + str(count_total) + ". Following user " + list.rstrip())
                    file_op.write_to_file(st + " " + str(count_total) + ". Following user " + list.rstrip(), '\\log.log')
                    file_op.write_to_file(list.rstrip(),'\\lists\\black_list.txt')
                    old_count=count
                    count=count_total//count_pause
                    count_total=count_total+1
                    if count!=old_count:
                        file_op.write_to_file("Pause " + str(time_to_sleep) + " sec", '\\log.log')
                        print("Pause " + str(time_to_sleep) + " sec")
                        time.sleep(time_to_sleep)
                    else:
                        random_pause = random.randrange(pause_min, pause_max, 1)
                        file_op.write_to_file(st + " Pause " + str(random_pause) + " sec", '\\log.log')
                        print(st + " " + "Pause " + str(random_pause) + " sec")
                        time.sleep(random_pause)
                else:
                    if not_arab==False:
                        file_op.write_to_file('                    Arab_detected!!! ' + test , '\\log.log',1)
                        file_op.write_to_file(list.rstrip(),'\\lists\\black_list.txt')
                        time.sleep(2)
                    else:
                        print(st + " " + "Error: Allready followed user " + list.rstrip())
                        file_op.write_to_file(st + " " + "Error: Allready followed user " + list.rstrip(), '\\log.log')
                        file_op.write_to_file(list.rstrip(),'\\lists\\black_list.txt')
                        time.sleep(2)
            else:
                print(st + " " + "Error: Not found user " + list.rstrip())
                file_op.write_to_file(st + " " + "Error: Not found user " + list.rstrip(), '\\log.log')
                time.sleep(5)
    else:
        print('The list is empty')
        file_op.write_to_file("The list is empty", '\\log.log')



elif TASK=='unfollow':
    unfollow_list_path='\\lists\\unfollow_list_' + USER + '.txt'
    if file_op.file_exist(unfollow_list_path)==False:
        getfollowers(USER)
    unfollow_list=file_op.read_from_file(unfollow_list_path)
    unfollow_list=list(set(unfollow_list))

    if len(unfollow_list)>=1:
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file('------------------------------', '\\log.log')
        file_op.write_to_file('------------------------------', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')
        file_op.write_to_file(' ', '\\log.log')

        print(str(len(unfollow_list)) + ' positions in unfollow list')
        file_op.write_to_file(str(len(unfollow_list))  + ' positions in unfollow list','\\log.log')

        api = InstagramAPI(USER, PASSWORD)
        api.login()

        for list in unfollow_list:
            list=str(list).rstrip()
            if count_total>=500:
                print('Complete!!!')
                file_op.write_to_file("Complete!!!", '\\log.log')
                file_op.remove_file(unfollow_list_path)
                api.logout()
                break
            user_id_dict=api.testplease(list)

            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            if user_id_dict['num_results']>=1:
                user_id_dict=user_id_dict['users']
                user_id=user_id_dict[0]['pk']
                for item in user_id_dict:
                    item_username=item['username']
                    following_status=False
                    if item_username==list.lower():
                        user_id=item['pk']
                        following_status=item['friendship_status']['following']
                        # not_arab=not_arabian()
                        break
                if following_status:
                    api.unfollow(user_id)
                    print(st + " " + str(count_total) + ". Unfollowing user " + list.rstrip())
                    file_op.write_to_file(st + " " + str(count_total) + ". Unfollowing user " + list.rstrip(), '\\log.log')
                    old_count=count
                    count=count_total//count_pause
                    count_total=count_total+1
                    if count!=old_count:
                        file_op.write_to_file("Pause " + str(time_to_sleep) + " sec", '\\log.log')
                        print("Pause " + str(time_to_sleep) + " sec")
                        time.sleep(time_to_sleep)
                    else:
                        random_pause = random.randrange(pause_min, pause_max, 1)
                        file_op.write_to_file(st + " Pause " + str(random_pause) + " sec", '\\log.log')
                        print(st + " " + "Pause " + str(random_pause) + " sec")
                        time.sleep(random_pause)
                else:
                    print(st + " " + "Error: Allready unfollowed from user " + list.rstrip())
                    file_op.write_to_file(st + " " + "Error: Allready unfollowed from user " + list.rstrip(), '\\log.log')
                    time.sleep(2)
            else:
                print("Error: Not found user " + list.rstrip())
                file_op.write_to_file(st + " " + "Error: Not found user " + list.rstrip(), '\\log.log')
                time.sleep(5)
    else:
        print('The list is empty')
        file_op.write_to_file("The list is empty", '\\log.log')
else:
    getfollowers(TASK)