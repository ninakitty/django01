# coding:utf-8
__author__ = 'nina'
__date__ = '2018/1/3 16:27'
from .models import EmailVerifyRecord, Banner
import xadmin
from xadmin import views

#在主app下的adminx.py下定义
# 打开主题
class BaseSetting(object):
    enable_themes = True  # 主题打开
    use_bootswatch = True  #


# 设备页面头和脚、左侧标签类型
class GlobalSetting(object):
    site_title = 'NINAKITTY'
    site_footer = '哈哈肚皮'
    menu_style = 'accordion'

#在各app下的adminx.py下定义
# 定义显示内容
class EmailVerifyRecordAdmin(object):
    # 显示列表
    list_display = ('code', 'email', 'send_type', 'send_time')
    # 搜索参数
    search_fields = ('code', 'email', 'send_type',)
    # 过滤列表
    list_filter = ('code', 'email', 'send_type', 'send_time')


class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ('title', 'image', 'url', 'index', 'add_time')
    list_filter = ('title', 'image', 'url', 'index', 'add_time')


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
