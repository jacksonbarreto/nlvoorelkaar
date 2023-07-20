

if __name__ == '__main__':
    classes = set(['c-card', 'c-card--offer', 'js-card'])
    print(classes)
    name = 'section'
    if {'c-card', 'c-card--offer', 'js-card'}.issubset(classes):
        print('yes')

    if name == 'section':
        print('yes name')