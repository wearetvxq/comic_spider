# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.parser import parse
import logging
import re

logger = logging.getLogger(__name__)

NORM_FORMAT = "%Y%m%d"
NORM_FORMAT_FULL = "%Y-%m-%d %H:%M:%S"

def norm_format(s, format=NORM_FORMAT_FULL):
    return datetime.strptime(s, format).strftime(NORM_FORMAT_FULL)

def get_datetime_from_format(s, command):
    if isinstance(command, basestring):
        return norm_format(s, command)

date_regex = {
    u'^.*?(\d+).*秒前.*$' : 'second',
    u'^.*?(\d+).*秒钟前.*$' : 'second',
    u'^.*?(\d+).*分钟前.*$' : 'minute',
    u'^.*?(\d+).*小时前.*$' : 'hour',
    u'^.*半小时前.*$' : 'halfhour',
    u'^.*?(\d+).*天前.*$' : 'day',
    u'^.*?(\d+).*周前.*$' : 'week',
    u'^.*?(\d+).*月前.*$' : 'month',
    u'^.*?刚刚.*$' : 'justnow',
    u'^.*?一天前.*$': 'lastday',
    u'^.*昨天.*$': 'lastday',
    u'^.*?两天前.*$': 'day2',
    u'^.*前天.*$': 'day2',
    u'^.*上周.*$' : 'lastweek',
    u'^.*今天.*$' : 'today',
    u'^.*?(\d+)月(\d+)日.*$' : 'someday',
    u'^.*?(\d+)-(\d+)-(\d+).*?(\d+):(\d+).*$' : 'special1',
}

date_patterns = {}
for regex, key in date_regex.items():
    date_patterns[re.compile(regex, re.DOTALL)] = key

def norm_special_date(s):
    logger.debug('--in norm special date : %s---' % s)
    for pattern, key in date_patterns.items():
        match = re.match(pattern, s)
        if match:
            logger.debug('matched : %s' % key)
            res_obj = None
            if key == 'second':
                res_obj = datetime.now() - timedelta(seconds=int(match.group(1)))
            elif key == 'minute':
                res_obj = datetime.now() - timedelta(minutes=int(match.group(1)))
            elif key == 'halfhour':
                res_obj = datetime.now() - timedelta(minutes=30)
            elif key == 'hour':
                res_obj = datetime.now() - timedelta(hours=int(match.group(1)))
            elif key == 'day':
                res_obj = datetime.now() - timedelta(days=int(match.group(1)))
            elif key == 'week':
                res_obj = datetime.now() - timedelta(weeks=int(match.group(1)))
            elif key == 'month':
                res_obj = datetime.now() - timedelta(days=30*int(match.group(1)))
            elif key == 'lastday':
                res_obj = datetime.now() - timedelta(days=1)
            elif key == 'day2':
                res_obj = datetime.now() - timedelta(days=2)
            elif key == 'lastweek':
                res_obj = datetime.now() - timedelta(days=7)
            elif key == 'today':
                res_obj = datetime.now()
            elif key == 'someday':
                res_obj = datetime(year=2016, month=int(match.group(1)), day=int(match.group(2)))
            elif key == 'justnow':
                res_obj = datetime.now()
            elif key == 'special1':
                res_obj = datetime(year=int(match.group(1)),
                                   month=int(match.group(2)),
                                   day=int(match.group(3)),
                                   hour=int(match.group(4)),
                                   minute=int(match.group(5)))
            result = res_obj
            #logger.warn('---%s---%s------' % (s, result))
            return result


def get_datetime_from_timestamp(s):
    try:
        return datetime.fromtimestamp(int(s)).strftime(NORM_FORMAT_FULL)
    except Exception:
        return

def norm_date(s, rule):
    if rule:
        return norm_date(get_datetime_from_format(s, rule),None)
    if isinstance(s, basestring):
        try:
            res = parse(s)
            if res:
                return res
            else:
                return norm_special_date(s)
        except Exception:
            return norm_special_date(s)


def get_current_datetime():
    return datetime.now().strftime(NORM_FORMAT_FULL)

def datetime_to_date(s):
    return datetime.strptime(s, NORM_FORMAT_FULL).strftime(NORM_FORMAT)

def get_current_date():
    return datetime.now().strftime(NORM_FORMAT)

def older_than(first_date, second_date):
    return datetime.strptime(first_date, NORM_FORMAT_FULL) < datetime.strptime(second_date, NORM_FORMAT_FULL)

def get_first_day_of_month(date_obj):
    date_obj = date_obj - timedelta(int(date_obj.strftime('%d'))-1)
    return date_obj.strftime(NORM_FORMAT)

def get_weekday_for_date(date_obj):
    weekday = int(date_obj.strftime('%w'))
    if weekday == 0:
        weekday = 7
    return weekday

def get_first_day_of_week(date_obj):
    weekday = get_weekday_for_date(date_obj)
    date_obj = date_obj - timedelta(weekday-1)
    return date_obj.strftime(NORM_FORMAT)

def calculate(s, format=NORM_FORMAT_FULL):
    date_obj = datetime.strptime(s, format)
    first_day_of_month = get_first_day_of_month(date_obj)
    first_day_of_week = get_first_day_of_week(date_obj)
    weekday = str(get_weekday_for_date(date_obj))
    publishdate = datetime_to_date(s)
    return first_day_of_month, first_day_of_week, weekday, publishdate

if __name__ == '__main__':
    print type(norm_date('2015-12-12 12:12',None))
    # print calculate('20160717')


