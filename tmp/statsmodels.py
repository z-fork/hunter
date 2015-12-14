# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
from operator import itemgetter

import MySQLdb
import numpy as np
import pandas as pd
from patsy.highlevel import dmatrices, dmatrix
from sklearn.linear_model import LogisticRegression


from collections import OrderedDict

QUESTION_TYPE_PRACTICE = 1  # 练题模式
QUESTION_TYPE_CHALLENGE = 2  # 挑战模式
QUESTION_TYPE_REVIEW = 3  # 查看模式
QUESTION_TYPE_MOCK_EXAM = 4  # 模拟考试

QUESTION_TYPES = [
    (QUESTION_TYPE_PRACTICE, '练题模式'),
    (QUESTION_TYPE_CHALLENGE, '挑战模式'),
    (QUESTION_TYPE_REVIEW, '查看模式'),
    (QUESTION_TYPE_MOCK_EXAM, '模拟考试')
]

'''
四六级用到的题型常量, 四大类题型分组的常量以 K_XX_GROUP 表示

K_COMPOSITION_GROUP = 1
K_LISTEN_GROUP = 2
K_READING_GROUP = 3
K_TRANSLATION_GROUP = 4

K_COMPOSITION = 1019

K_SHORT_DIALOG = 1012  # 听力-短对话
K_LONG_DIALOG = 1014  # 听力-长对话
K_LONG_DIALOG_QUESTION = 1028  # 听力-长对话-问题
K_LISTEN_PASSAGE = 1025
K_LISTEN_PASSAGE_QUESTION = 1026
K_DICTATION = 1009 # 重写四六级题型中的短文听写
K_DICTATION_QUESTION = 1010

K_WORD_SELECT = 1011 # 重写四六级题型中的选词填空
K_WORD_SELECT_QUESTION = 1031
K_PARAGRAPH_INFO_MATCH = 1039  # 段落信息匹配
K_PARAGRAPH_INFO_MATCH_QUESTION = 1040  # 段落信息匹配-问题
K_READING_IN_DEPTH = 1020  # 仔细阅读
K_READING_QUESTION = 1021  # 仔细阅读-问题

K_TRANSLATION = 1016  # 翻译

'''

K_COMPOSITION_GROUP = 1
K_LISTEN_GROUP = 2
K_READING_GROUP = 3
K_TRANSLATION_GROUP = 4

# 题目类型
K_CHOICE_STEM = 1000

K_LISTENING = 1008  # 听力大类
K_LISTEN_DICTATION = 1009
K_LISTEN_DICTATION_ANSWER = 1010

K_DICTATION = 1009  # 重写四六级题型中的短文听写
K_DICTATION_QUESTION = 1010


K_WORD_SELECT = 1011  # 重写四六级题型中的选词填空
K_WORD_SELECT_QUESTION = 1031

K_SELECT_WORD = 1011  # 选词填空(共享答案的选择题)
K_SHORT_DIALOG = 1012  # 听力-短对话
K_SHORT_DIALOG_QUESTION = 1013  # 听力-短对话-问题
K_LONG_DIALOG = 1014  # 听力-长对话
K_TRANSLATION = 1016  # 翻译
K_SINGLE_CHOICE = 1017  # 单项选择题
K_COMPOSITION = 1019

K_READING = 1077  # 阅读大类
K_READING_IN_DEPTH = 1020  # 仔细阅读
K_READING_QUESTION = 1021  # 仔细阅读-问题
K_ESSAY = 1025
K_LISTEN_PASSAGE = 1025
K_ESSAY_QUESTION = 1026
K_LISTEN_PASSAGE_QUESTION = 1026
K_LONG_DIALOG_QUESTION = 1028  # 听力-长对话-问题
K_SELECT_WORD_QUESTION = 1031  # 选词填空-问题
K_CONTEXT_COMPLETE = 1034  # 补全对话/短文
K_COMPLETE_QUESTION = 1035  # 补全对话/短文-问题
K_INFORMATION = 1037  # 主观听取信息
K_INFORMATION_ANSWER = 1038  # 主观听取信息-答案

K_PARAGRAPH_INFO_MATCH = 1039  # 段落信息匹配
K_PARAGRAPH_INFO_MATCH_QUESTION = 1040  # 段落信息匹配-问题

K_TASK = 1041  # 任务型写作/阅读
K_TASK_QUESTION = 1042  # 任务型写作/阅读-问题

K_READ_EXPRESSION = 1043  # 阅读表达
K_READ_EXPRESSION_QUESTION = 1044  # 阅读表达-问题

K_PASSAGE_BLANK = 1045  # 短文填词&语法填空&补全对话
K_PASSAGE_BLANK_QUESTION = 1046  # 短文填词&语法填空&补全对话

K_CLOZE = 1047  # 完形填空
K_CLOZE_QUESTION = 1048

K_SENTENCE = 1083  # 大类 & 小类
K_SENTENCE_TRANSFORMATION = 1081  # 句型转换
K_SENTENCE_ANALYSIS = 1082  # 句子成分分析
K_SENTENCE_ANSWER = 1051  # 完成句子-答案
K_TRANSLATION_SENTENCE = 1052  # 单句翻译
K_TRANSLATION_SENTENCE_QUESTION = 1053  # 单句翻译-答案

K_SENTENCE_QUESTION = 1090

K_SELECT_WORD_DICTATION = 1054  # 选词填空-上下文填空题 (Note: 区分选词填空选择题)
K_SELECT_WORD_DICTATION_QUESTION = 1055  # 选词填空-上下文填空题-问题

K_DISJOINT_SELECT_WORD = 1073  # 选词填空，有公共选项，答案是文本形式
K_DISJOINT_SELECT_WORD_QUESTION = 1074  # 选词填空问题

K_COMPOSE_SENTENCE = 1056  # 连词成句
K_COMPOSE_SENTENCE_QUESTION = 1057  # 连词成句-答案

K_JUDGE = 1058  # 判断型阅读
K_JUDGE_QUESTION = 1059  # 判断型阅读-问题

K_IMAGE_DICTATION = 1061  # 根据图片写句子
K_IMAGE_DICTATION_QUESTION = 1062  # 根据图片写句子-问题

K_SPELL_WORD = 1064  # 单词拼写
K_SPELL_WORD_ANSWER = 1065  # 单词拼写-答案

K_DISJOINT_MULTI_CHOICE_CONTEXT = 1066  # 共享答案一问多空选择题
K_DISJOINT_MULTI_CHOICE_QUESTION = 1067  # 共享答案一问多空选择题-问题

K_CORRECTION = 1070  # 改错题
K_CORRECTION_ANSWER = 1071  # 改错题-答案

K_INFO_MATCH = 1084  # 信息匹配（主旨与段落匹配）
K_INFO_MATCH_QUESTION = 1085

K_IMPORTING_ENGLISH_STEM = 1111  # 从第三方数据库导入的英语题目

# -------华丽的分割线-------NOTE: 所有题型的KIND常量请写在该分割线上面------华丽的分割线----------

# 四六级题目类型
CET_QUESTION_KINDS = {
    K_COMPOSITION,
    K_SHORT_DIALOG,
    K_LONG_DIALOG,
    K_ESSAY,
    K_LISTEN_DICTATION,
    K_SELECT_WORD,
    K_PARAGRAPH_INFO_MATCH,
    K_READING_IN_DEPTH,
    K_TRANSLATION,
}

# 题目审核状态
K_EDITING = 3000
K_SUBMITTED = 3001
K_CHECKED = 3002
K_APPROVED = 3003
K_DISCARDED = 3004
K_REJECTED = 3005
K_REEDITING = 3012

K_STATE_DICT = {
    K_EDITING: "录入中",
    K_SUBMITTED: "待初审",
    K_CHECKED: "待复审",
    K_APPROVED: "已入库",
    K_DISCARDED: "已废除",
    K_REJECTED: "被驳回",
    K_REEDITING: "初审驳回",
}

# 来源类型
SOURCE_DEFAULT = 0
SOURCE_ZH_MATH = 1
SOURCE_ZH_ENGLISH = 2

SOURCE_TYPES = OrderedDict([
    (SOURCE_DEFAULT, '默认'),
    (SOURCE_ZH_MATH, '志鸿数学'),
    (SOURCE_ZH_ENGLISH, '志鸿英语'),
])

# 考试类型
EXAM_TYPE_DEFAULT = 0

EXAM_CET4 = 1
EXAM_CET4_MOCK = 2
EXAM_CET6 = 3
EXAM_CET6_MOCK = 4
EXAM_GK = 5
EXAM_GK_MOCK = 6
EXAM_ZK = 7
EXAM_ZK_MOCK = 8
EXAM_MID_TERM = 9
EXAM_MID_TERM_MOCK = 10
EXAM_MONTHLY = 11
EXAM_SYNC_TEST = 12
EXAM_HK = 13
EXAM_COMPETITION = 14
EXAM_MKZH = 15

EXAM_TYPES = OrderedDict([
    (EXAM_TYPE_DEFAULT, '无'),
    (EXAM_CET4, "四级真题"),
    (EXAM_CET4_MOCK, "四级模拟题"),
    (EXAM_CET6, "六级真题"),
    (EXAM_CET6_MOCK, "六级模拟题"),
    (EXAM_GK, "高考真题"),
    (EXAM_GK_MOCK, "高考模拟题"),
    (EXAM_ZK, "中考真题"),
    (EXAM_ZK_MOCK, "中考模拟题"),
    (EXAM_MID_TERM, "期中"),
    (EXAM_MID_TERM_MOCK, "期末"),
    (EXAM_MONTHLY, "月考"),
    (EXAM_SYNC_TEST, "同步测试"),
    (EXAM_HK, "会考"),
    (EXAM_COMPETITION, "竞赛题"),
    (EXAM_MKZH, "模块综合"),
])

OFFICIAL_EXAM_TYPES = OrderedDict([
    (EXAM_CET4, "四级真题"),
    (EXAM_CET6, "六级真题"),
])

CET_EXAM_TYPES = OrderedDict([
    (EXAM_TYPE_DEFAULT, '无'),
    (EXAM_CET4, "四级真题"),
    (EXAM_CET4_MOCK, "四级模拟题"),
    (EXAM_CET6, "六级真题"),
    (EXAM_CET6_MOCK, "六级模拟题"),
])

#----------------------------------------

QUESTION_CONF = {
    K_COMPOSITION:{
        'table':'composition',
        'question_table':None,
        'sub_type':None,
        'has_stem_difficulty':True
    },

    K_SHORT_DIALOG:{
        'table':'short_dialog',
        'question_table':None,
        'sub_type':None,
        'has_stem_difficulty':True
    },

    K_LONG_DIALOG:{
        'table':'long_dialog',
        'question_table':'long_dialog_question',
        'sub_type':K_LONG_DIALOG_QUESTION,
        'has_stem_difficulty':False
    },

    K_LISTEN_PASSAGE:{
        'table':'listen_passage',
        'question_table':'listen_passage_question',
        'sub_type':K_LISTEN_PASSAGE_QUESTION,
        'has_stem_difficulty':False
    },

    K_DICTATION:{
        'table':'dictation',
        'question_table':'dictation_question',
        'sub_type':K_DICTATION_QUESTION,
        'has_stem_difficulty':True
    },

    K_WORD_SELECT:{
        'table':'word_select',
        'question_table':'word_select_question',
        'sub_type':K_WORD_SELECT_QUESTION,
        'has_stem_difficulty':True
    },

    K_PARAGRAPH_INFO_MATCH:{
        'table':'info_match',
        'question_table':'info_match_question',
        'sub_type':K_PARAGRAPH_INFO_MATCH_QUESTION,
        'has_stem_difficulty':True
    },

    K_READING_IN_DEPTH:{
        'table':'intensive_reading',
        'question_table':'intensive_reading_question',
        'sub_type':K_READING_QUESTION,
        'has_stem_difficulty':True
    },

    K_TRANSLATION:{
        'table':'translation',
        'question_table':None,
        'sub_type':None,
        'has_stem_difficulty':True
    }
}


cet_dev_conf = {
    'host': 'sqlproxy',
    'user': 'cet',
    'passwd': 'TOEFLeasier',
    'db': 'cet_production',
    'port': 4406,
    'charset': 'utf8mb4'
}

conn = MySQLdb.connect(**cet_dev_conf)

sql = ('select id parent_log_id, user_id uid, target_kind qtype, '
       'target_id qid, seconds, record_time, '
       'n_right, n_wrong from practice_log limit 10000')

A = pd.read_sql_query(sql, conn)
A = A[(A.seconds > 2) & (A.seconds < 1800)]

B = A.groupby('uid').size().reset_index()
B.columns = ['uid', 'q_count']
B = B[B.q_count >= 3]

print A.head()
print B.head()
M = pd.merge(A, B)

print M.head()


def _pick_latest_log(df):
    res = df.sort('record_time').tail(1)
    return res[['parent_log_id', 'seconds', 'n_right', 'n_wrong']]

M = M.groupby(['uid', 'qtype', 'qid']).apply(_pick_latest_log).reset_index()
M = M[(M.n_right != 0) | (M.n_wrong != 0)]
M = M[['parent_log_id', 'uid', 'seconds']]

print M.head()

sql = ('select parent_log_id, user_id, parent_kind, parent_id, '
       'target_id, status from practice_log_detail limit 10000')
X = pd.read_sql_query(sql, conn)
X.columns = ['parent_log_id', 'uid', 'qtype', 'qid', 'sub_id', 'status']

print X.head()

M = pd.merge(X, M)

print M.head()

EMPTY = 0
WRONG = 1
RIGHT = 2

print '-' * 10

def get_qinfo_by_type(conn, configs, qtype):
    conf = configs[qtype]
    if conf['has_stem_difficulty']:
        sql = 'select id, difficulty from %s where status = %s'
    else:
        sql = 'select id, 0 from %s where status = %s'
    A = pd.read_sql_query(sql % (conf['table'], K_APPROVED), conn)
    A.columns = ['qid', 'q_diff']

    qinfo = dict()
    for _, row in A.iterrows():
        qid, q_diff = map(int, row)
        # q_diff, sub_info
        # 大题难度, 小题信息 {sub_id:sub_diff}
        qinfo[qid] = [q_diff, dict()]

    if conf['question_table']:
        sql = 'select stem_id, id, difficulty from %s'
        B = pd.read_sql_query(sql % conf['question_table'], conn)
        B.columns = ['qid', 'sub_id', 'sub_diff']
        for _, row in B.iterrows():
            qid, sub_id, sub_diff = map(int, row)
            # 如果 qid 不在 qinfo 说明不是入库的题, 需要跳过
            if qid not in qinfo:
                continue
            qinfo[qid][1][sub_id] = sub_diff

    ans = []
    for qid, (q_diff, sub_info) in qinfo.iteritems():
        if not sub_info:
            ans.append((qtype, qid, qid, 1, q_diff))
            continue
        n_question = len(sub_info)
        for sub_id, sub_diff in sub_info.iteritems():
            diff = q_diff if not sub_diff else sub_diff
            ans.append((qtype, qid, sub_id, n_question, diff))

    return ans


sql = ('select target_kind, target_id, exam_type '
       'from origin where exam_type != %s') % EXAM_TYPE_DEFAULT
df = pd.read_sql_query(sql, conn)
origin = dict()
for _, row in df.iterrows():
    qtype, qid, exam_type = map(int, row)
    origin.setdefault(qtype, {})[qid] = exam_type

qinfo = dict()
for qtype in QUESTION_CONF.keys():
    res = get_qinfo_by_type(conn, QUESTION_CONF, qtype)
    for qtype, qid, sub_id, n_question, diff in res:
        exam_type = origin.get(qtype, {}).get(qid, EXAM_TYPE_DEFAULT)
        if exam_type == EXAM_TYPE_DEFAULT:
            continue
        qinfo[(qtype, qid, sub_id)] = (n_question, diff, exam_type)

practice_log = []

# TODO 没有细看
for _, row in M.iterrows():
    parent_log_id, uid, qtype, qid, sub_id, status, seconds = map(int, row)
    if status == EMPTY:
        continue
    correct = 1 if status == RIGHT else 0
    res = qinfo.get((qtype, qid, sub_id), None)
    if res is None:
        continue
    n_question, diff, exam_type = res
    seconds = float(seconds) / n_question
    line = (uid, qtype, qid, sub_id, seconds, correct)
    practice_log.append(line)

practice_log = pd.DataFrame(practice_log)
practice_log.columns = ['uid', 'qtype', 'qid', 'sub_id', 'seconds', 'correct']

user_avg = practice_log.drop(['qid', 'sub_id'], axis=1).groupby(
    ['uid', 'qtype']).mean().reset_index()
user_avg.columns = ['uid', 'qtype', 'avg_time', 'avg_correct']
item_avg = practice_log.drop('uid', axis=1).groupby(
    ['qtype', 'qid', 'sub_id']).mean().reset_index()
item_avg.columns = ['qtype', 'qid', 'sub_id', 'avg_time', 'avg_correct']

print practice_log.head()
#    uid  qtype   qid  sub_id  seconds  correct
# 0  119   1014  1655    3090    47.00        0
# 1  119   1014  1655    3091    47.00        0
# 2  119   1014   268     505    42.75        1
# 3  119   1014   268     506    42.75        1
# 4  119   1014   268     507    42.75        1


def dump_user_feature(redis_db, user_profile, user_avg):
    '''
    将用户特征存入 redis, json 格式, 每个 uid key 解析后为:
    [
        gender,
        location,
        {
            qtype: (avg_time, avg_correct)
        }
    ]
    同时返回结果 dict 方便输出 practice_log 训练数据
    {qtype: (avg_time, avg_correct)} 的默认值也会存储到 redis 中
    '''
    res = dict()
    # 对于没有练题记录的用户, 用某种题型的全体均值作为默认值
    default_score = dict()
    # 对于没有练题记录的题型, 则用全部记录的均值作为默认值
    global_score_list = []

    for _, row in user_avg.iterrows():
        uid, qtype, avg_time, avg_correct = row
        uid, qtype = int(uid), int(qtype)
        res.setdefault(uid, {})[qtype] = (avg_time, avg_correct)
        default_score.setdefault(qtype, []).append((avg_time, avg_correct))
        global_score_list.append((avg_time, avg_correct))

    for qtype, score_list in default_score.iteritems():
        avg_time = np.mean(map(itemgetter(0), score_list))
        avg_correct = np.mean(map(itemgetter(1), score_list))
        default_score[qtype] = (avg_time, avg_correct)
    global_avg_time = np.mean(map(itemgetter(0), global_score_list))
    global_avg_correct = np.mean(map(itemgetter(1), global_score_list))
    global_default_score = (global_avg_time, global_avg_correct)

    # 处理第一次上线新题型没有练题数据的尴尬
    for qtype in CET_QUESTION_KINDS:
        if qtype not in default_score:
            default_score[qtype] = global_default_score

    user_feature = dict()
    for uid, (gender, location_id) in user_profile.iteritems():
        score = res.get(uid, default_score)
        for qtype in CET_QUESTION_KINDS:
            if qtype not in score:
                score[qtype] = default_score[qtype]
        feature = [gender, location_id, score]
        user_feature[uid] = feature

    #     key = CET_USER_FEATURE_KEY % uid
    #     value = json.dumps(feature)
    #     redis_db.set(key, value)
    #
    # # 将默认值也存入 redis, 供没有特征的用户使用
    # for qtype, score in default_score.iteritems():
    #     value = json.dumps(score)
    #     redis_db.hset(CET_USER_DEFAULT_FEATURE_KEY, qtype, value)

    return user_feature


def dump_question_feature(redis_db, qinfo, item_avg):
    '''
    将题目特征存入 redis, json 格式, 解析后为:
    {
        'qtype:qid:sub_id': [n_question, diff, exam_type, avg_time, avg_correct]
    }
    '''
    res = dict()
    # 对于没有练题记录的题目, 用该题型的全体均值作为默认值
    default_score = dict()
    # 对于没有练题记录的题型, 则用全部记录的均值作为默认值
    global_score_list = []

    for _, row in item_avg.iterrows():
        qtype, qid, sub_id  = map(int, row[:3])
        item_id = '%s:%s' % (qid, sub_id)
        avg_time, avg_correct = row[3:5]
        res.setdefault(qtype, {})[item_id] = (avg_time, avg_correct)
        default_score.setdefault(qtype, []).append((avg_time, avg_correct))
        global_score_list.append((avg_time, avg_correct))

    for qtype, score_list in default_score.iteritems():
        avg_time = np.mean(map(itemgetter(0), score_list))
        avg_correct = np.mean(map(itemgetter(1), score_list))
        default_score[qtype] = (avg_time, avg_correct)
    global_avg_time = np.mean(map(itemgetter(0), global_score_list))
    global_avg_correct = np.mean(map(itemgetter(1), global_score_list))
    global_default_score = (global_avg_time, global_avg_correct)

    for qtype in CET_QUESTION_KINDS:
        if qtype not in default_score:
            default_score[qtype] = global_default_score

    question_feature = dict()
    for k, v in qinfo.iteritems():
        qtype, qid, sub_id = k
        item_id = '%s:%s' % (qid, sub_id)
        n_question, diff, exam_type = v
        try:
            avg_time, avg_correct = res[qtype].get(item_id, default_score[qtype])
        except KeyError:
            continue
        feature = [n_question, diff, exam_type, avg_time, avg_correct]

        field = '%s:%s:%s' % (qtype, qid, sub_id)
        question_feature[field] = feature
    #     value = json.dumps(feature)
    #     redis_db.hset(CET_QUESTION_FEATURE_KEY, field, value)
    #
    # # 将默认值也存入 redis, 供没有特征的题目使用
    # for qtype, score in default_score.iteritems():
    #     value = json.dumps(score)
    #     redis_db.hset(CET_QUESTION_DEFAULT_FEATURE_KEY, qtype, value)

    return question_feature

sql = ('select id location_id, type, parent_id from location '
       'where type != 0 order by type')
A = pd.read_sql_query(sql, conn)
location_info = dict()
for _, row in A.iterrows():
    location_id, type, parent_id = map(int, row)
    if type <= 2:
        location_info[location_id] = location_id
    else:
        location_info[location_id] = location_info[parent_id]


sql = 'select id uid, gender, location_id from user_profile'
A = pd.read_sql_query(sql, conn)

user_profile = dict()
for _, row in A.iterrows():
    uid, gender, location_id = row
    uid = int(uid)
    gender = 0 if np.isnan(gender) else int(gender)
    location_id = 0 if np.isnan(location_id) else int(location_id)
    location_id = location_info.get(location_id, location_id)
    user_profile[uid] = [gender, location_id]


def dump_practice_log(practice_log, user_feature, question_feature):
    out = open('practice_log', 'w')
    for _, row in practice_log.iterrows():
        uid, qtype, qid, sub_id = map(int, row[:4])
        seconds, correct = row[4:6]
        gender, location_id, u_score = user_feature[uid]
        u_avg_time, u_avg_correct = u_score[qtype]
        field = '%s:%s:%s' % (qtype, qid, sub_id)
        if field not in question_feature:
            continue  # 会有部分已废弃题目的练题脏数据
        feature = question_feature[field]
        n_question, diff, exam_type, q_avg_time, q_avg_correct = feature

        line = [uid, qtype, qid, sub_id, correct, seconds,
                gender, location_id, u_avg_time, u_avg_correct,
                n_question, diff, exam_type, q_avg_time, q_avg_correct]
        line = "\t".join(map(str, line))
        print >> out, line
    out.close()


user_feature = dump_user_feature(None, user_profile, user_avg)
question_feature = dump_question_feature(None, qinfo, item_avg)
dump_practice_log(practice_log, user_feature, question_feature)

df = pd.read_csv('practice_log', sep='\t', header=None)
df.columns = ['uid', 'qtype', 'qid', 'sub_id', 'correct',
              'seconds', 'gender', 'location_id', 'u_avg_time',
              'u_avg_correct', 'n_question', 'diff', 'exam_type',
              'q_avg_time', 'q_avg_correct']

print df.head()


LR_FORMULA = ('correct ~ C(qtype) + seconds + C(gender) + C(location_id) '
              '+ u_avg_time + u_avg_correct + n_question + diff '
              '+ C(exam_type) + q_avg_time + q_avg_correct')


y, X = dmatrices(LR_FORMULA, df)
y = np.ravel(y)
model = LogisticRegression(penalty='l1', C=0.1, fit_intercept=True)
model = model.fit(X, y)
print model.score(X, y)

