import xlsxwriter
import pickle
from sklearn.metrics import classification_report
import numpy as np

workbook = xlsxwriter.Workbook('TN1.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:T', 100000)

def to_label(int_label):
    if int_label == 0:
        return 'CLEAN'
    elif int_label == 1:
        return 'OFFENSIVE'
    else:
        return 'HATE'


header = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'center',
    'border': 2})
    
merge = workbook.add_format({
    'align': 'center',
    'valign': 'center',
    'border': 1})

bold = workbook.add_format({
    'bold': 1
})

wrong = workbook.add_format({
    'border': 1,
    'fg_color': 'red'
})

correct = workbook.add_format({
    'border': 1, 
    'fg_color': 'white'
})

miss = workbook.add_format({
    'border': 1, 
    'fg_color': 'yellow'
})
border = workbook.add_format({
    'border': 1
})

method = ['origin', 'spelling_mistake','skip-gram', 'cbow', 'fasttext_fb', 'fasttext_vne', 'symspell', 'google']
data = []

test_y = pickle.load(open('test_y.dump', 'rb'))

# tạo cái header
for p, j in enumerate(method):
    worksheet.set_column(chr(ord('C') + p*2) + ':' + chr(ord('D') + p*2), 20)
    worksheet.merge_range(chr(ord('C') + p*2) + '1' + ':' + chr(ord('D') + p*2) + '1', j, header)
    
worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 15)
worksheet.write('A1', 'STT', header)

# đọc dữ liệu lên
# for i in method:
#     data.append(open('NB_edited_test\/'+i+'.txt', encoding='utf8').read().split('-----------------------\n\n'))

# ghi stt
for index in range(4069):
    worksheet.merge_range('A' + str(2 + index*2) + ':' + 'A' + str(3 + index*2), 
                            str(index), merge)
    worksheet.write('B' + str(2 + index*2), 'Label', bold)
    worksheet.write('B' + str(3 + index*2), 'Content:', bold)

report = ''
test_y = np.argmax(test_y, axis=1)

# ghi vào file excel
for i_md in range(len(method)):
    # đọc data lên
    data = open(r'result\test.txt'.replace('test', method[i_md]), encoding='utf8').read().split('\n------------------\n')
    for index, md_rt in enumerate(data[:-1]):
        # temp = md_rt.split('\n')
        fm = ''
        md_rt = md_rt.split('\n')
        if int(md_rt[0]) == test_y[index]:
            fm = correct
        else:
            fm = wrong
        # else:
        #     fm = miss
        worksheet.write(str(chr(ord('C')+ i_md*2)) + str(2 + index*2), 
                            'Predict: ' + to_label(int(md_rt[0])), fm)

        worksheet.write(str(chr(ord('D')+ i_md*2)) + str(2 + index*2), 
                            'Target: ' + to_label(test_y[index]), fm)

        worksheet.merge_range(str(chr(ord('C')+ i_md*2)) + str(3 + index*2) + ':' + str(chr(ord('D')+ i_md*2)) + str(3 + index*2), 
                            md_rt[1], fm)
        

        # if temp[2].split('\t')[0].replace('Từ bị sửa:    ', '').replace('set()', '').strip() != '':
        #     worksheet.merge_range(str(chr(ord('O')+ i_md)) + str(2 + index*4) + ':' + chr(ord('O')+ i_md) + str(5 + index*4), 
        #                             'CÓ', merge)
        # else:
        #     worksheet.merge_range(str(chr(ord('O')+ i_md)) + str(2 + index*4) + ':' + chr(ord('O')+ i_md) + str(5 + index*4), 
        #                             'KHÔNG', merge)


workbook.close()

# # data = open('cbow_dn.txt', encoding='utf8').read().split('----------------------------\n\n')
# # for index, i in enumerate(data):
# #     i = i.split('\n')
    



# # print(chr(ord('N')+ 1))
