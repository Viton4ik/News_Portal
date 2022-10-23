
from django import template

register = template.Library()


censorship_list = ['спорт', 'австралия', 'согласие', 'рублев']

@register.filter()
def censor(word):
   word_list_adapted = []
   try:
      word_no_space = word.strip()
      word_list = word_no_space.split()
      for word in word_list:
         word_adapted = word.lower()
         if word_adapted in censorship_list:
            word_censored = word[0] + '*' * (len(word_adapted)-1)
            word_list_adapted.append(word_censored)
         else:
            word_censored = word
            word_list_adapted.append(word_censored)
         corrected = " ".join(word_list_adapted)
      return corrected
   except AttributeError as e:
      return f"ErrorMessage: {e}. Please use only 'str'!"

