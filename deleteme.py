print('Do not run this program unless you want to DELETE it.')
print('Are you sure you want to delete this program?')
if input('Enter "DELETE" to delete it or anything else to exit.\n') == 'DELETE':
    import os, time
    for i in range(10, 0, -1):
        print('\n' * 100)
        print('Deleting in', i)
        if i <= 5:
            print('CAUTION! DELETING SOON!')
        time.sleep(1)
    os.unlink('deleteme.py')
    print('\n' * 100, 'Deleted')
    time.sleep(1)
    for i in range(10, 0, -1):
        print('\n' * 100)
        print('Quitting in', i)
        time.sleep(1)
else:
    print('Thank you')