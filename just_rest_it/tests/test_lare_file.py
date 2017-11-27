# -*- coding: utf-8 -*-

"""
问题描述：读取2G文件，文件每行有一个整数，请找出最大的10个数字

"""
import os
import random
import unittest


def trunk_reader(file, chunkSize=2048):
    """分块儿读取"""
    while True:
        trunk_data = file.read(chunkSize)
        if not trunk_data:
            break
        yield trunk_data


class TestReadLargeFile(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test.data'
        self.max_num = 100
        self.max_top_10 = []
        self.line_num_list = []

        # file exist skip create
        if os.path.exists(self.test_file):
            return

        # create large file
        with open(self.test_file, 'w') as test_file:
            # for i in xrange(0, 1024 * 1024 * 1024 / 3):
            for i in xrange(0, 10000000):
                random_int = random.randint(0, self.max_num)
                test_file.write('%s\n' % random_int)

    def tearDown(self):
        print sorted(self.max_top_10, reverse=True), '\n', sorted(set(self.line_num_list), reverse=True)[:10]

    @unittest.skip("skip memory error")
    def test_1_MemoryError(self):
        # 一次性读取大文件，抛出MemoryError
        with self.assertRaises(MemoryError) as err:
            with open(self.test_file, 'r') as f:
                f.read()

    def add_or_update_top_list(self, new_num):
        """更新topN"""

        # 去重
        if new_num in self.max_top_10:
            return 'exist'

        # 先填充10个
        if len(self.max_top_10) < 10:
            self.max_top_10.append(new_num)

            # 初始列表填充完毕，做一次排序
            if len(self.max_top_10) == 10:
                self.max_top_10.sort()
            return 'add'

        # 查找替换
        for i, num in enumerate(self.max_top_10):
            if new_num > num:
                self.max_top_10.insert(i, new_num)
                self.max_top_10 = self.max_top_10[:-1]
                break
        else:
            return 'skiped'

        return 'replaced'

    # @unittest.skip("skip")
    def test_2_MaxLine(self):
        max_line_num = 0
        print self.test_file
        with open(self.test_file, 'r') as f:
            # 缓存IO和内存管理
            for line in f:
                line_num = int(line.strip('\n'))
                # self.line_num_list.append(line_num)
                self.add_or_update_top_list(line_num)
                # if line_num > max_line_num:
                #     max_line_num = line_num
                # self.assertLessEqual(max_line_num, self.max_num)

    @unittest.skip("skip")
    def test_trunk_reader(self):
        print self.test_file
        with open(self.test_file, 'r') as f:
            for chunk in trunk_reader(f):
                chunk_list = chunk.split('\n')
                for num in chunk_list:
                    if num:
                        self.add_or_update_top_list(int(num))
                # print chunk_list
                # map(lambda x: self.assertIsInstance(int(x), int), chunk_list)
