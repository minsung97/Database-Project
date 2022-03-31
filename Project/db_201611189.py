import pymysql
import csv
conn = pymysql.connect(host = 'localhost', user='root', password='3746', db='db_201611189')
curs = conn.cursor(pymysql.cursors.DictCursor)

# user 데이터 삽입
f = open('u.user.tsv','r')
rdr = csv.reader(f, delimiter = '|')
tsvlist = list(rdr)

for row in tsvlist:
    user_id = (row[0])
    user_age = (row[1])
    user_gender = (row[2])
    user_occupation = (row[3])
    user_zipcode = (row[4])
    
    sql = "insert into User (userid,age,gender,occupation,zipcode) values (%s,%s,%s,%s,%s)"
    user_list = (user_id,user_age,user_gender,user_occupation,user_zipcode)
    curs.execute(sql,user_list)
    #db의 변화 저장 
    conn.commit()
    row = curs.fetchone()

f.close()

# item 데이터 삽입
f = open('u.item.tsv','r',encoding = "ISO-8859-1")
rdr = csv.reader(f,delimiter = '|')
tsvlist = list(rdr)

for row in tsvlist:
    movie_id = (row[0])
    movie_title = (row[1])
    movie_release = (row[2])
    movie_video_release = (row[3])
    movie_url = (row[4])
    movie_genre = (row[5])+(row[6])+(row[7])+(row[8])+(row[9])+(row[10])+(row[11])+(row[12])+(row[13])+(row[14])+(row[15])+(row[16])+(row[17])+(row[18])+(row[19])+(row[20])+(row[21])+(row[22])+(row[23])

    sql = "insert into Item (movieid,title,releasedate,v_releasedate,url,genre) values (%s,%s,%s,%s,%s,%s)"
    item_list = (movie_id,movie_title,movie_release,movie_video_release,movie_url,movie_genre)
    curs.execute(sql,item_list)
    #db의 변화 저장
    conn.commit()
    row = curs.fetchone()

f.close()
# Data 데이터 삽입
f = open('u.data.tsv','r')
rdr = csv.reader(f, delimiter = '\t')
tsvlist = list(rdr)

for row in tsvlist:
    data_user_id = (row[0])
    data_movie_id = (row[1])
    rating = (row[2])
    timestamp = (row[3])

    sql = "insert into Data (userid,movieid,rating,timestamp) values (%s,%s,%s,%s)"
    data_list = (data_user_id,data_movie_id,rating,timestamp)
    curs.execute(sql,data_list)
    #db의 변화 저장
    conn.commit()
    row = curs.fetchone()

f.close()

# Genre 데이터 삽입
f = open('u.genre.tsv','r')
rdr = csv.reader(f, delimiter = '|')
tsvlist = list(rdr)
tsvlist = list(filter(None, tsvlist))

for row in tsvlist:
    genre_name = (row[0])
    genre_code = (row[1])
    
    sql = "insert into Genre (genrename,genrecode) values (%s,%s)"
    genre_list = (genre_name,genre_code)
    curs.execute(sql,genre_list)
    #db의 변화 저장
    conn.commit()
    row = curs.fetchone()
f.close()

# Occupation 데이터 삽입
f = open('u.occupation.tsv','r')
rdr = csv.reader(f, delimiter = '|')
tsvlist = list(rdr)

for row in tsvlist:
    occupation_name = (row[0])
    
    sql = "insert into Occupation (occupationname) values (%s)"
    occupation_list = (occupation_name)
    curs.execute(sql,occupation_list)
    #db의 변화 저장
    conn.commit()
    row = curs.fetchone()

f.close()

# 검색 기능
print("검색할 장르를 입력하세요 : ")
s_genre = input()
print("검색할 사용자의 직업을 입력하세요 : ")
s_occupation = input()
print("검색할 영화의 최소 평점을 입력하세요 : ")
s_min = input()
print("검색할 영화의 최대 평점을 입력하세요 : ")
s_max = input()
print("정렬 방식을 선택하세요 1. 영화 제목 오름차순 2. 영화 제목 내림차순 3. 평점 오름차순 4.평점 내림차순 5.vote 수 오름차순 6. vote 수 내림차순: ")
s_sortby = input()

if s_min == '':
    s_min = 1
if s_max == '':
    s_max = 5
    
#사용자가 입력한 장르가 포함된 movieid를 저장하는 list  answer_genre
if s_genre != '':
    sql = "select genrecode from Genre where genrename = '%s'"%(s_genre)
    curs.execute(sql)
    row= curs.fetchone()
    s_genre_num = row["genrecode"]

answer_genre = []
sql_genre = "select * from Item i"
curs.execute(sql_genre)
row = curs.fetchone()
if s_genre == '':
    while row:
      answer_genre.append(row["movieid"])
      row = curs.fetchone()
else: 
    while row:
        original_genre = list(row["genre"])
        if original_genre[s_genre_num] == '1':
            answer_genre.append(row["movieid"])
        row = curs.fetchone()

#사용자가 입력한 직업을 가진 사람을 저장하는 리스트 answer_occupation
answer_occupation = []
sql_occupation = "select * from User u"
curs.execute(sql_occupation)
row = curs.fetchone()
if s_occupation == '':
    while row:
        answer_occupation.append(row["userid"])
        row = curs.fetchone()
else:
    while row:
         original_occupation = (row["occupation"])
         if original_occupation == s_occupation:
             answer_occupation.append(row["userid"])
         row = curs.fetchone()

#answer_genre에 있는 moiveid만 data테이블에서 필터링
genre_count = 0
filter_genre = []
while genre_count < len(answer_genre):
    sql = "select * from Data d where movieid = '%s'"%(answer_genre[genre_count])
    curs.execute(sql)
    row = curs.fetchone()
    while row:  
        filter_genre.append(row)
        row = curs.fetchone()
    genre_count = genre_count + 1

#answer_occupation에 있는 moiveid만 data테이블에서 필터링
occupation_count = 0
filter_occupation = []
while occupation_count < len(answer_occupation):
    sql = "select * from Data d where userid = '%s'"%(answer_occupation[occupation_count])
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        filter_occupation.append(row)
        row = curs.fetchone()
    occupation_count = occupation_count + 1

#각 필터링의 공통부분 구하기
answer_filter = [x for x in filter_genre if x in filter_occupation]

#장르와 직업에 관하여 필터링이 완료된 테이블을 집계 함수를 이용해 평점 계산
sql = "create table Answer (userid int, movieid int, rating int, timestamp int)"
curs.execute(sql)
answer_filter_count = 0
while answer_filter_count < len(answer_filter):
    sql = "insert into Answer (userid,movieid,rating,timestamp) values (%s,%s,%s,%s)"
    answer_list = (answer_filter[answer_filter_count]["userid"],answer_filter[answer_filter_count]["movieid"],answer_filter[answer_filter_count]["rating"],answer_filter[answer_filter_count]["timestamp"])
    curs.execute(sql,answer_list)
    conn.commit()
    answer_filter_count = answer_filter_count + 1

if s_sortby == '1':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s' order by i.title"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
if s_sortby == '2':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s' order by i.title desc"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
if s_sortby == '3':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s'order by AVG(a.rating)"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
if s_sortby == '4':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s'order by AVG(a.rating) desc"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
if s_sortby == '5':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s'order by COUNT(a.rating)"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
if s_sortby == '6':
    sql = "select i.title, AVG(a.rating), COUNT(a.rating) from Answer a, Item i where a.movieid = i.movieid group by a.movieid having AVG(a.rating) >='%s' and AVG(a.rating) <= '%s'order by COUNT(a.rating) desc"%(s_min,s_max)
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        print("영화제목: %s, 평점 : %s 평가횟수 : %s "%(row['title'],row['AVG(a.rating)'],row['COUNT(a.rating)']))
        row = curs.fetchone()
sql = "drop table answer"
curs.execute(sql)
curs.close()
conn.close()