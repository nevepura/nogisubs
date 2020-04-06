'''
I got issues with overlapping subtitles on .srt files. 
The extension for chrome browser Substitial does not read them well.
So I can edit subs. No more overlapping!
'''

from sys import argv


def extract_times(line):
    parts = line.split()
    current_time_first = parts[0]
    current_time_last = parts[2]
    return current_time_first, current_time_last


def manage_time_intersection(time1, time2):
    '''time1 must be minor or equal than time2. If it is greater, time1 is set equal to time2'''
    # parse integer numbers from time strings
    hours1 = int(time1[0:2])
    hours2 = int(time2[0:2])

    minutes1 = int(time1[3:5])
    minutes2 = int(time2[3:5])
    
    seconds1 = int(time1[6:8])
    seconds2 = int(time2[6:8])
    
    milliseconds1 = int(time1[9:12])
    milliseconds2 = int(time2[9:12])
    
    # if time1 > time2
    if hours1 > hours2 or \
        hours1 == hours2 and minutes1 > minutes2 or \
        hours1 == hours2 and minutes1 == minutes1 and seconds1 > seconds2 or \
        hours1 == hours2 and minutes1 == minutes1 and seconds1 == seconds2 and milliseconds1 > milliseconds2: 
            # equalize
            time1 = time2
    return time1, time2

def create_new_subs(f, input_file_name):
    '''creates a new subtitle file where the subtitles are separated and never overlap'''
    # read file from end to beginning
    lines = f.readlines()
    # reverse the order, because I wanna overwrite the previous subtitles
    lines.reverse() 

    # saving the times of the previous subtitle. Init with zero
    next_time_first = None # first time of the next subtitle
    # next_time_last = None # last time of the next subtitle
    output_lines = []
    
    for line in lines:       
        if '-->' in line: # the line contains times: must check if they are ok
            # extract first and last
            current_time_first, current_time_last = extract_times(line)
            
            # skip if there is no next time
            if next_time_first is not None:
                # manage time intersection between previous and current time; 
                current_time_last, next_time_first = manage_time_intersection(current_time_last, next_time_first)
                
                # Special case: two subs with same time. In this case, the previous sub is crushed to 0 seconds length.
                # This case is not treated.

                # Compose the line with fair times
                line = current_time_first + ' --> ' + current_time_last + '\n'
            
            # end of the cycle: set current time as previous
            next_time_first = current_time_first
            # next_time_last = current_time_last
 
        # append line to output lines
        output_lines.append(line)
    
    # reverse back to the original order
    output_lines.reverse()

    # write to output
    output_text = ''.join(output_lines)
    output_file_name = input_file_name[:-4] + '_edited' +'.srt'
    with open(output_file_name, 'w') as out:
        out.write(output_text)
    print('"{}" created successfully!'.format(output_file_name))


def main():
    script , input_file_name = argv
    
    f = open(input_file_name)
    create_new_subs(f, input_file_name)


if __name__ == '__main__':
    main()