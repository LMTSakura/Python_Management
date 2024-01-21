import requests     # pip install requests
import parsel       # pip install parsel
import csv
import time

def py_requests():
    with open('汽车之家.csv', mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['card_name', 'cards_unit', 'price', 'original_price', 'href_url', 'img_url'])
    headers = {
        'cookie': 'fvlid=1678707796259lUxyb5ctia8Y; sessionid=88abf095-f918-4e12-9837-cf8e61024732; area=430112; che_sessionid=1476DA7D-0E1A-4DB6-A0E5-94074A95603C%7C%7C2023-03-13+19%3A43%3A16.765%7C%7C0; listuserarea=0; sessionip=175.13.226.104; Hm_lvt_d381ec2f88158113b9b76f14c497ed48=1699272164; UsedCarBrowseHistory=0%3A49368425; userarea=0; sessionvisit=80b96168-6a79-46b4-b8a5-64adbde2fdda; sessionvisitInfo=88abf095-f918-4e12-9837-cf8e61024732|www.che168.com|102179; che_sessionvid=BE7B0EF0-7E60-4A60-9FBE-5CE182AA0FD2; ahpvno=8; Hm_lpvt_d381ec2f88158113b9b76f14c497ed48=1699276565; ahuuid=1993BFC6-651A-471B-A2F0-549B12314CE8; showNum=56; v_no=59; visit_info_ad=1476DA7D-0E1A-4DB6-A0E5-94074A95603C||BE7B0EF0-7E60-4A60-9FBE-5CE182AA0FD2||-1||-1||59; che_ref=0%7C0%7C0%7C0%7C2023-11-06+21%3A16%3A04.741%7C2023-03-13+19%3A43%3A16.765; sessionuid=88abf095-f918-4e12-9837-cf8e61024732',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    for page in range(100):
        url = f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/?pvareaid=102179#currengpostion'
        #发送请求
        response = requests.get(url, headers=headers)
        #提取数据
        html_data = response.text
        time.sleep(2)
        # JSON格式的数据 -> 结构化数据 (根据层级关系取值) 字典取值 列表取值
        # 网页源代码 -> 非结构化数据
        # 所有的车辆信息 全部都在 li里面
        # 那我是不是可以先将 所有的 li 提取到
        # //ul[@class="viewlist_ul"]/li
        select = parsel.Selector(html_data)
        # 拿到所有的li
        lis = select.xpath('//ul[@class="viewlist_ul"]/li')
        for li in lis:
            card_name = li.xpath('string(.//h4[@class="card-name"])').get()
            cards_unit = li.xpath('string(.//p[@class="cards-unit"])').get()
            price = li.xpath('string(.//span[@class="pirce"])').get()
            original_price = li.xpath('string(.//s)').get()
            href_url = li.xpath('.//a[@class="carinfo"]/@href').get()
            img_url = li.xpath('.//img/@src').get()
            print(card_name, cards_unit, price, original_price, href_url, img_url)
            # 多页采集 保存数据
            with open('汽车之家.csv', mode='a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow([card_name, cards_unit, price, original_price, href_url, img_url])
# py_requests()