import re
percent_p = ''''{super:'{simple_int:5, simple_string:"XYZ", simple_enum:FIRST}, some_queue:'{5, 6, 7}, obj_i:pp_example::obj@2_2}'''

output = '''{super:{simple_int:5, simple_string:"XYZ", simple_enum:"FIRST"}, some_queue:[5,6,7], obj_i:"pp_example::obj@2_2"}'''

def find_curly_pairs(s):
    pair = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '{':
            pstack.append(i)
        elif c == '}':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            pair[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return pair

curly_pairs = find_curly_pairs(percent_p)

print(curly_pairs)

no_single_semi=re.compile("[^:]:[^:]")

for open,close in curly_pairs.items():
  curly_contents = percent_p[open+1:close]

  if no_single_semi.search(curly_contents):
    # replace '{ with {
    percent_p = percent_p[:open-1] + ' {' + percent_p[open+1:]
  else:
    #replace '{ with [
    percent_p = percent_p[:open-1] + ' [' + percent_p[open+1:]
    percent_p = percent_p[:close] + ']' + percent_p[close+1:]

# turn :: into something really unlikely

percent_p = percent_p.replace("::", "@@@@@@")

# if value is not a list (i.e. starts with [,), or a nested dict (starts with {) or is only numbers or is already a string, enclose it in string

all_tokens_re=re.compile("([^\[^\]^\{^\}^\:^,^ ]+)")
number_re=re.compile("^[0-9]+$")

def convert_tokens(token):
    actual_token = token.group()

    if actual_token[0] == '"':
        return actual_token

    if number_re.match(actual_token):
        return actual_token

    return '"' + actual_token + '"'

almost_json = all_tokens_re.sub(convert_tokens,percent_p)

almost_json = almost_json.replace("@@@@@@", "::")

print (almost_json)

import json
json.loads(almost_json)
