import xlsxwriter

workbook = xlsxwriter.Workbook('hate_offensive_dong_nghia.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:T', 100000)


header = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'center'})
    
merge = workbook.add_format({
    'align': 'center',
    'valign': 'center'})

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

worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 10)
worksheet.set_column('C:D', 40)
worksheet.set_column('E:F', 40)
worksheet.set_column('G:H', 40)
worksheet.set_column('I:J', 40)
worksheet.set_column('K:L', 40)
worksheet.set_column('M:N', 40)
worksheet.set_column('O:O', 10)
worksheet.set_column('P:P', 10)
worksheet.set_column('Q:Q', 10)
worksheet.set_column('R:R', 10)
worksheet.set_column('S:S', 10)
worksheet.set_column('T:T', 10)


worksheet.write('A1', 'STT', header)
worksheet.merge_range('C1:D1', 'Skip-gram', header)
worksheet.merge_range('E1:F1', 'Cbow', header)
worksheet.merge_range('G1:H1', 'Fasttext_VNE', header)
worksheet.merge_range('I1:J1', 'Fasttext_FB', header)
worksheet.merge_range('K1:L1', 'SymSpell', header)
worksheet.merge_range('M1:N1', 'Google', header)
worksheet.write('O1', 'KQ_skipgram', header)
worksheet.write('P1', 'KQ_cbow', header)
worksheet.write('Q1', 'KQ_fasttextvne', header)
worksheet.write('R1', 'KQ_fasttextfb', header)
worksheet.write('S1', 'KQ_symspell', header)
worksheet.write('T1', 'KQ_google', header)

# workbook.close()

method = ['skip-gram', 'cbow', 'fasttextvne', 'fasttextfb', 'symspell', 'google']
data = []

# đọc dữ liệu lên
for i in method:
    data.append(open('hate_offensive\/'+i+'_dn.txt', encoding='utf8').read().split('----------------------------\n\n'))

# ghi stt
for index in range(len(data[0][:-1])):
    worksheet.merge_range('A' + str(2 + index*4) + ':' + 'A' + str(5 + index*4), 
                            str(index), merge)
    worksheet.write('B' + str(2 + index*4), 'Gải thích:', bold)
    worksheet.write('B' + str(3 + index*4), 'Câu sửa:', bold)
    worksheet.write('B' + str(4 + index*4), 'Câu gốc:', bold)
    worksheet.write('B' + str(5 + index*4), 'Câu sai:', bold)
# ghi vào file excel
for i_md in range(len(method)):
    for index, md_rt in enumerate(data[i_md][:-1]):
        temp = md_rt.split('\n')
        fm = ''
        if temp[0] == 'ĐÚNG':
            fm = correct
        elif temp[0] == 'SAI':
            fm = wrong
        else:
            fm = miss
        worksheet.write(str(chr(ord('C')+ i_md*2)) + str(2 + index*4), 
                            temp[1].split('\t')[0].replace('Từ sai:  ', ''), fm)
        worksheet.write(str(chr(ord('D')+ i_md*2)) + str(2 + index*4), 
                            temp[1].split('\t')[1].replace(' Từ gốc: ', ''), fm)

        worksheet.merge_range(str(chr(ord('C')+ i_md*2)) + str(3 + index*4) + ':' + chr(ord('D')+ i_md*2) + str(3 + index*4), 
                                temp[2].replace('Câu sửa: ', ''),fm)

        worksheet.merge_range(str(chr(ord('C')+ i_md*2)) + str(4 + index*4) + ':' + chr(ord('D')+ i_md*2) + str(4 + index*4), 
                                temp[3].replace('Câu gốc: ', ''), fm)

        worksheet.merge_range(str(chr(ord('C')+ i_md*2)) + str(5 + index*4) + ':' + chr(ord('D')+ i_md*2) + str(5 + index*4), 
                                temp[4].replace('Câu sai: ', ''), fm)  

        worksheet.merge_range(str(chr(ord('O')+ i_md)) + str(2 + index*4) + ':' + chr(ord('O')+ i_md) + str(5 + index*4), 
                                temp[0], merge)



workbook.close()

# data = open('cbow_dn.txt', encoding='utf8').read().split('----------------------------\n\n')
# for index, i in enumerate(data):
#     i = i.split('\n')
    



# print(chr(ord('N')+ 1))
