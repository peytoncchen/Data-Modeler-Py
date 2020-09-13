# Functions to export everything to xlsx

# Copyright (C) 2020 Peyton Chen

import xlsxwriter

def prepares5anddV(s5Inputs, dVResults): 
    #Modified version of preparetxt to prepare for write to xlsx
    result = []

    for i in range(len(s5Inputs[0])):
        temp = []
        temp.append(i+1)
        temp.append(int(s5Inputs[0][i]))

        for j in range(len(s5Inputs[1][i])):
            temp.append(int(s5Inputs[1][i][j]))

        temp.append(dVResults[i])
        result.append(temp)
    return result


def writetoxlsx(s1Inputs, s2Inputs, s3Inputs, s4Inputs, s4labels, s5Inputs, multiRun, 
fstring, fpwrstring, pstring, labels, errorResults, filename):
    #In one function, writes everything to xlsx 
    with xlsxwriter.Workbook(filename + '.xlsx') as workbook:
        sofar1 = 0
        sofar2 = 0
        worksheet = workbook.add_worksheet('Data Modeler Results')
        stepformat = workbook.add_format({'bold': True, 'bg_color': '#C6EFCE'})
        resultformat = workbook.add_format({'bold': True})
        runformat = workbook.add_format({'bold': True, 'bg_color': '#ADD8E6'})

        worksheet.write(0, 0, 'Form implementation generated from reading data from Data Modeler for Power Calculations software v1.0', resultformat)

        #Step 1
        worksheet.write(1, 0, 'Step 1', stepformat)
        worksheet.write(2, 0, 'Total Measurements')
        worksheet.write(2, 1, int(s1Inputs[0]))
        worksheet.write(3, 0, 'Number of treatments')
        worksheet.write(3, 1, int(s1Inputs[1]))
        worksheet.write(4, 0, 'Number of blocking factors')
        worksheet.write(4, 1, int(s1Inputs[2]))
        worksheet.write(5, 0, 'Name of measurement')
        worksheet.write(5, 1, s1Inputs[3])
        worksheet.write(6, 0, 'Name of dependent variable')
        worksheet.write(6, 1, s1Inputs[4])

        worksheet.set_column(0, 0, 22)
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 12)
        worksheet.set_column(4, 4, 12)
        worksheet.set_column(5, 5, 12)
        
        #Step 2
        worksheet.write(1, 3, 'Step 2: Blocking', stepformat)
        for i in range(len(s2Inputs[0])):
            worksheet.write(2+i, 3, s2Inputs[0][i])
            worksheet.write(2+i, 4, int(s2Inputs[1][i]))

        sofar1 += len(s2Inputs[0]) + 10

        #Error Results
        worksheet.write(1, 7, 'Generated Error', stepformat)
        worksheet.set_column(7, 7, 14)
        worksheet.set_column(8, 8, 14)
        sofarerror = 0
        for i, lst in enumerate(errorResults):
            for j, error in enumerate(lst):
                worksheet.write(2+j+sofarerror, 7, s2Inputs[0][i] + ' ' + str(j+1))
                worksheet.write(2+j+sofarerror, 8, error)
            sofarerror += len(lst)

        
        #Step 3
        worksheet.write(9, 0, 'Step 3: Error SDs', stepformat)
        worksheet.write(10, 0, 'Total error SD:')
        worksheet.write(10, 1, float(s3Inputs[0]))
        for i in range(1, len(s3Inputs)):
            worksheet.write(10+i, 0, s2Inputs[0][i-1] + ' error SD')
            worksheet.write(10+i, 1, float(s3Inputs[i]))
        
        #Step 4
        worksheet.write(9, 3, 'Step 4: Treatment', stepformat)
        worksheet.write(9, 4, 'Treatment labels', stepformat)
        worksheet.write(9, 5, 'Means', stepformat)
        for i in range(len(s4Inputs)):
            worksheet.write(10+i, 3, 'Treatment ' + str(i+1))
            if s4labels[i]:
                worksheet.write(10+i, 4, s4labels[i])
            worksheet.write(10+i, 5, float(s4Inputs[i]))
        
        sofar2 += len(s4Inputs) + 10

        if sofar1 > sofar2:
            sofar = sofar1
        else: 
            sofar = sofar2
        
        #If F-tests have been run:
        if fpwrstring:
            worksheet.write(sofar+3, 3, 'Power for fixed effect f-test from GLM is estimated as', resultformat)
            worksheet.write(sofar+4, 3, fpwrstring.strip())

        if fstring:
            worksheet.write(sofar+3, 0, 'GLM f-test results', resultformat)
            flst = fstring.split('\n')
            for i, item in enumerate(flst):
                worksheet.write(sofar+4+i, 0, item.strip())
            sofar += (len(flst) + 2)
        
        #If pairwise t-test pwr has been run:
        if pstring:
            worksheet.write(sofar+3, 0, 'Power for pairwise t-tests between treatments from GLM are estimated as', resultformat)
            plst = pstring.split('\n')
            for i, item in enumerate(plst):
                worksheet.write(sofar+4+i, 0, item)
            sofar += (len(plst) + 3)
        
        #Time for storing runs
        if multiRun:
            worksheet.write(sofar+3, 0, 'Run results', runformat)
            for k,label in enumerate(labels): #writes the labels
                worksheet.write(sofar+3, k+1, label, resultformat) #shift over one column since placing Run # labels in first column
            for i,run in enumerate(multiRun):
                worksheet.write(sofar+5, 0, 'Run ' + str(i+1), resultformat)
                lst = prepares5anddV(s5Inputs, run)
                for line in lst:
                    worksheet.write_number(sofar+5, 1, i+1)
                    for j,val in enumerate(line):
                        worksheet.write_number(sofar+5, j+2, val)
                        worksheet.set_column(j+2, j+2, 12) #To ensure all columns used are same width
                    sofar += 1 #next line