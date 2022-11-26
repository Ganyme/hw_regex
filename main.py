import re
import csv
from pprint import pprint

def reading_file():
  with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    return contacts_list


def create_new_contacts_list():
  result_contacts_list = []

  for card in contacts_list:
    result_card = []
    lastname = re.search(r'^[А-ЯЁ][а-яё]*(в|ва|ин|на)', card[0])
    if lastname != None:
      result_card.append(lastname.group())
    else:
      result_card.append('')

    str_name = (re.search(r'(,| )[А-ЯЁ][а-яё]*', card[0]) or re.search(r'^[А-ЯЁ][а-яё]*', card[1]))
    if str_name != None:
      str_name = str_name.group()
      pattern1 = r'(,| )([А-ЯЁ][а-яё]*)'
      firstname = re.sub(pattern1, r'\2', str_name)
      result_card.append(firstname)
    else:
      result_card.append('')

    str_surname = (re.search(r'(,| )[А-ЯЁ][а-яё]*(ич|на)', card[0]) or re.search(r'(,| )[А-ЯЁ][а-яё]*(ич|на)', card[1]) or re.search(r'^[А-ЯЁ][а-яё]*', card[2]))
    if str_surname != None:
      str_surname = str_surname.group()
      pattern2 = r'(,| )([А-ЯЁ][а-яё]*(ич|на))'
      surname = re.sub(pattern2, r'\2', str_surname)
      result_card.append(surname)
    else:
      result_card.append('')

    organization = (re.search(r'[М][а-яё]{5}', card[3]) or re.search(r'[А-Я]{3}', card[3]))
    if organization != None:
      result_card.append(organization.group())
    else:
      result_card.append('')

    position = card[4]
    result_card.append(position)

    pattern = "(\+7|8)\s*\(*(\d{3})\)*[-\s]*(\d{3})\-*(\d{2})\-*(\d{2})\s*\(*(\доб.)*\s*(\d{4})*\)*"
    phone = re.sub(pattern, r'+7(\2)\3-\4-\5 \6\7', card[5])
    if phone != None:
      result_card.append(phone)

      result_card.append(card[6])

    result_contacts_list.append(result_card)

  return result_contacts_list


def delete_dubles(result_contacts_list):
  result_contacts_list[0][0] = 'lastname'
  result_contacts_list[0][1] = 'firstname'
  result_contacts_list[0][2] = 'surname'
  result_contacts_list[0][3] = 'organization'

  for card in result_contacts_list:
    for card1 in result_contacts_list[(result_contacts_list.index(card)+1):]:
      if card[0] == card1[0] and card[1] == card1[1]:
        if card1[3] != '':
          card[3] = card1[3]
        if card1[4] != '':
          card[4] = card1[4]
        if card1[5] != '':
          card[5] != card[5]
        if card1[6] != '':
          card[6] = card1[6]
        result_contacts_list.remove(card1)

  return result_contacts_list


def create_file(result_contacts_list):
  with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_contacts_list)

if __name__ == '__main__':
  contacts_list = reading_file()
  result_contacts_list = create_new_contacts_list()
  cleared_cl = delete_dubles(result_contacts_list)
  create_file(result_contacts_list)
