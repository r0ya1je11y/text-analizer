from konlpy.tag import Komoran
from collections import Counter
from wordcloud import WordCloud
import csv
import matplotlib.pyplot as plt
import matplotlib.backends


def Alert():
    print("==========================================================")
    print("")
    print("  1. 텍스트 명사 빈도 분석")
    print("  2. 워드클라우드 제작")
    print("")
    

def GetFlieText():
    while(True):
        file_name = input("분석할 TXT 파일 이름을 입력해주세요 (확장자명 제외): ")

        try:
            input_file = open('./data/' + file_name + '.txt', 'r', encoding="utf-8")
            break
        except:
            print("잘못된 파일명입니다!")
    
    raw_text = input_file.read()
    input_file.close()
    
    return raw_text


def GetFileCsv():
    while(True):
        file_name = input("분석할 CSV 파일 이름을 입력해주세요 (확장자명 제외): ")
        try:
            with open('./data/' + file_name + '.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return_data = []
                for row in reader:
                    return_data.append(list(row.items()))
            break
        except:
            print("잘못된 파일명입니다!")
            
    return return_data


def MakeFile(noun_list):
    file_name = input("출력할 파일 이름을 입력해주세요 (확장자명 제외): ")
    result_file = open('./data/' + file_name + '.csv', 'w', encoding="utf-8")
    result_file.write('{},{}\n'.format('단어', '횟수'))
    for tag in noun_list:
        noun = tag['tag']
        count = tag['count']
        result_file.write('{},{}\n'.format(noun, count))
    
    print("파일 출력이 완료되었습니다.")
    result_file.close()


def GetTags():
    print("==========================================================")
    print("[텍스트 명사 빈도 분석]", end="\n\n")
    
    text = GetFlieText()
    
    print("분석 중입니다.....")
    nlpy = Komoran(userdic='./dic/dic.user')    # 사용자 사전 등록
    nouns = nlpy.nouns(text)    # text에서 명사만 추출
    for i, v in enumerate(nouns):
        if len(v) < 2:  # 2보다 작은 길이의 명사 제거
            nouns.pop(i)
    count = Counter(nouns)
    print("분석 완료!")
    
    while(True):
        try:
            print_num = int(input("출력할 단어의 갯수를 입력해주세요 (정수): "))
            break
        except:
            print("잘못된 입력입니다!")
            
    noun_list = []
    words = dict(count.most_common(print_num))
    for key, value in words.items():
        temp = {'tag':key, 'count':value}
        noun_list.append(temp)
    
    MakeFile(noun_list)


def showWordcloud():
    print("==========================================================")
    print("[워드클라우드 제작]", end="\n\n")
    csv_data = GetFileCsv()

    frequency = {}
    for row in csv_data:
        frequency[row[0][1]] = int(row[1][1])
    print("생성 중입니다.....")
    
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color='white', colormap="Dark2", width=1500, height=1000).generate_from_frequencies(frequency)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
    print("생성 완료!")
    

if __name__ == '__main__':
    Alert()
    while(True):
        num = input("사용할 기능의 번호를 선택해주세요: ")
        if num is '1':
            GetTags()
            break
        elif num is '2':
            showWordcloud()
            break
        else:
            print("잘못된 번호입니다!", end="\n\n")
            continue