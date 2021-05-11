import xlsxwriter

workbook = xlsxwriter.Workbook('clean_goc.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:T', 100000)


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
    'border': 1,
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

method = ['skip-gram', 'cbow', 'fasttextvne', 'fasttextfb', 'symspell', 'google']

data = []

# tạo cái header
for index, i in enumerate(['', 'AB_', 'edited_']):
    for p, j in enumerate(method):
        if index != 0:
            worksheet.set_column(chr(ord('C')+ index*6 + p) + ':' + chr(ord('C')+ index*6 + p), 15)
        else:
            worksheet.set_column(chr(ord('C')+ index*6 + p) + ':' + chr(ord('C')+ index*6 + p), 40)
        worksheet.write(chr(ord('C')+ index*6 + p) + '1', i + j, header)

worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 15)
worksheet.write('A1', 'STT', header)

# đọc dữ liệu lên
for i in method:
    data.append(open('clean_goc\/'+i+'.txt', encoding='utf8').read().split('-----------------------\n\n'))

# ghi stt
for index in range(len(data[0][:-1])):
    worksheet.merge_range('A' + str(2 + index*4) + ':' + 'A' + str(5 + index*4), 
                            str(index), merge)
    worksheet.write('B' + str(2 + index*4), 'Thêm badwords:', bold)
    worksheet.write('B' + str(3 + index*4), 'Từ bị sửa:', bold)
    worksheet.write('B' + str(4 + index*4), 'Câu gốc:', bold)
    worksheet.write('B' + str(5 + index*4), 'Câu sửa:', bold)
# ghi vào file excel
for i_md in range(len(method)):
    for index, md_rt in enumerate(data[i_md][:-1]):
        temp = md_rt.split('\n')
        fm = ''
        if temp[0] == 'KHÔNG':
            fm = correct
        elif temp[0] == 'THÊM':
            fm = wrong
        # else:
        #     fm = miss
        worksheet.write(str(chr(ord('C')+ i_md)) + str(2 + index*4), 
                            temp[1].split('\t')[0].replace('Thêm Badword: ', '').replace('set()', ''), fm)

        worksheet.write(str(chr(ord('C')+ i_md)) + str(3 + index*4), 
                            temp[2].split('\t')[0].replace('Từ bị sửa:    ', '').replace('set()', ''), fm)

        worksheet.write(str(chr(ord('C')+ i_md)) + str(4 + index*4), 
                            temp[3].split('\t')[0].replace('Câu gốc:      ', ''), fm)
        
        worksheet.write(str(chr(ord('C')+ i_md)) + str(5 + index*4), 
                            temp[4].split('\t')[0].replace('Câu sửa:      ', ''), fm)

        worksheet.merge_range(str(chr(ord('I')+ i_md)) + str(2 + index*4) + ':' + chr(ord('I')+ i_md) + str(5 + index*4), 
                                temp[0], merge)

        if temp[2].split('\t')[0].replace('Từ bị sửa:    ', '').replace('set()', '').strip() != '':
            worksheet.merge_range(str(chr(ord('O')+ i_md)) + str(2 + index*4) + ':' + chr(ord('O')+ i_md) + str(5 + index*4), 
                                    'CÓ', merge)
        else:
            worksheet.merge_range(str(chr(ord('O')+ i_md)) + str(2 + index*4) + ':' + chr(ord('O')+ i_md) + str(5 + index*4), 
                                    'KHÔNG', merge)



workbook.close()

# # data = open('cbow_dn.txt', encoding='utf8').read().split('----------------------------\n\n')
# # for index, i in enumerate(data):
# #     i = i.split('\n')
    



# # print(chr(ord('N')+ 1))
