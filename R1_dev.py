import re
from time import sleep
from urllib.parse import urlencode
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import unittest


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Chrome(executable_path=r'F:\software\python\python3.7\Tools\geckodriver\chromedriver.exe')
        self.driver = webdriver.Firefox(
            executable_path=r'F:\software\python\python3.7\Tools\geckodriver\geckodriver.exe')
        self.information_list = ['d7fb564b02ac684f01f73375e32b7e9a',
                                 '%E6%B7%B1%E5%9C%B3%E7%9B%92%E5%AD%90%E4%BF%A1%E6%81%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8']
        self.url = r'file:///C:/Users/user/Desktop/html/company_getinfos.html'

    def test_search_in_python_org(self):
        self.login()
        print(self.get_invested_enterprise_information())

    def login(self):
        self.driver.get(
            'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&client_id=101188807&redirect_uri=http%3A%2F%2Fwww.qichacha.com%2Fuser_callbackqq&state=4fe189a24145c0848fb69c3a1da72c51&scope=get_user_info,add_share')
        self.driver.switch_to.frame('ptlogin_iframe')
        self.driver.find_element(By.ID, "img_out_qq_code").click()
        sleep(5)

    # def get_company_information_and_store(self, company_unique, company_name):
    #     self.information_list.append(company_unique)
    #     self.information_list.append(urlencode(company_name))
    #     pass

    def get_invested_enterprise_information(self):
        information_list = ['ba8406a2a2af01b3ac8d030c3f14c305',
                            '天津三快科技有限公司']
        url = "https://www.qcc.com/company_getinfos?unique=d7fb564b02ac684f01f73375e32b7e9a&companyname=%E6%B7%B1%E5%9C%B3%E7%9B%92%E5%AD%90%E4%BF%A1%E6%81%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&p=1&tab=base&box=touzi"

        xpath_list = ["//td[@width='235']//span[@class='seo font-14']",
                      "//td[@width='235']//a[@target='_blank']", "//td[@width='82']"]
        url = []

        url.append("https://www.qcc.com/company_getinfos?unique=" + information_list[0] + "&companyname=" +
                   information_list[1] + "&p=")
        url.append("&tab=base&box=touzi")

        invested_enterprise_order = ['被投资企业名称', 'href', '投资比例']
        name_of_invested_enterprise_list = []
        invested_enterprise_href_list = []
        investment_ratio_list = []


        information = self.get_information(url, xpath_list, True)

        count = 1
        for tem_next in information:
            if count % 3 == 1:
                for i in tem_next:
                    name_of_invested_enterprise_list.append(i.text)
            elif count % 3 == 2:
                for i in tem_next:
                    invested_enterprise_href_list.append(i.get_attribute('href'))
            elif count % 3 == 0:
                for i in tem_next:
                    investment_ratio_list.append(i.text)
            count += 1

        # get the text from element
        return invested_enterprise_order, self.get_the_control_company_information(name_of_invested_enterprise_list,
                                                                                   invested_enterprise_href_list,
                                                                                   investment_ratio_list)


    def get_information(self, url, xpath_list, page_exit_flag):
        # the url_list will be depart by page variable
        if page_exit_flag:
            page = 1
            page_flag = True
            while page_flag == True:
                self.driver.get(url[0] + str(page) + url[1])
                if self.driver.find_elements_by_xpath(xpath_list[0]):
                    for xpath in xpath_list:
                        yield self.driver.find_elements_by_xpath(xpath)
                    page = page + 1
                else:
                    page_flag = False
        else:
            self.driver.get(url)
            for xpath in xpath_list:
                yield self.driver.find_elements_by_xpath(xpath)

    # delete the company whose percentage less than 50%
    def get_the_control_company_information(self, name_of_invested_enterprise_list, invested_enterprise_href_list,
                                            investment_ratio_list):
        if len(investment_ratio_list) == len(name_of_invested_enterprise_list):
            index = len(investment_ratio_list)
        else:
            raise RuntimeError('two list length not equal')
        i = 0
        while i < index:
            percentage = investment_ratio_list[i]
            if "%" in percentage:
                float_percentage = float(percentage.strip("%")) / 100
                if float_percentage < 0.5:
                    name_of_invested_enterprise_list.pop(i)
                    invested_enterprise_href_list.pop(i)
                    investment_ratio_list.pop(i)
                    index = index - 1
                    continue
            else:
                raise RuntimeError('the object is not a percentage object!')
            i = i + 1

        # get the unique
        index = len(invested_enterprise_href_list)
        i = 0
        while i < index:
            invested_enterprise_href_list[i] = re.findall(r"firm/(.+?).html", invested_enterprise_href_list[i])[0]
            # print(invested_enterprise_href_list[i])
            i = i + 1

        return name_of_invested_enterprise_list, invested_enterprise_href_list, investment_ratio_list

    def get_the_software_copyright_information(self):
        software_copyrigh_order = ['软件名称', '版本号', '发布日期', '软件简称', '登记批准日期']
        software_name = self.driver.find_elements_by_xpath("//td[@width='278']")

        version_number = self.driver.find_elements_by_xpath("//td[@width='9%']")
        pubilc_time = self.driver.find_elements_by_xpath("//td[@width='140']")
        software_abbreviation = self.driver.find_elements_by_xpath("//td[@width='16%']")
        register_time = self.driver.find_elements_by_xpath("//td[@width='150']")
        print(self.get_element_text(software_name))
        print(self.get_element_text(version_number))
        print(self.get_element_text(pubilc_time))
        print(self.get_element_text(software_abbreviation))
        print(self.get_element_text(register_time))
        pass

    def get_the_app_information(self):
        app_order = ['名称', '分类', '当前版本', '简介']
        app_name = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[1]")
        classification = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[2]")
        current_version = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[3]")
        brief_introduction = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::span[1]")
        print(self.get_element_text(app_name))
        print(self.get_element_text(classification))
        print(self.get_element_text(current_version))
        print(self.get_element_text(brief_introduction))
        pass

    def get_the_wechat_mini_program_information(self):
        mini_program_order = ['名称', '分类']
        mini_program_name = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[1]")
        classification = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[2]")
        print(self.get_element_text(mini_program_name))
        print(self.get_element_text(classification))

    def get_the_wechat_public_account(self):
        public_account_order = ['微信公众号', '微信id', '简介']
        name = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[1]")
        id = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[2]")
        brief_introduction = self.driver.find_elements_by_xpath("//img[@style='width: 66px;']//following::td[4]")
        print(self.get_element_text(name))
        print(self.get_element_text(id))
        print(self.get_element_text(brief_introduction))

    def get_the_website(self):
        weisite_order = ['网站名称', '网址', '域名', '审核日期']
        website_name = self.driver.find_elements_by_xpath("//td[@width='15%']")
        website_url = self.driver.find_elements_by_xpath("//td[@width='18%']//a")
        website_domain = self.driver.find_elements_by_xpath("//td[@width='13%']")
        audit_date = self.driver.find_elements_by_xpath("//td[@width='103']")
        print(self.get_element_text(website_name))
        print(self.get_element_text(website_url))
        print(self.get_element_text(website_domain))
        print(self.get_element_text(audit_date))

    def get_element_text(self, element_object):
        list = []
        for i in element_object:
            list.append(i.text)
        return list

    def tearDown(self):
        # self.driver.quit()
        pass


if __name__ == "__main__":
    unittest.main()
