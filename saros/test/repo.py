#!/usr/bin/python

# repo module contains saros db (i.e., the repo) states needed for unit tests.
# ##############################################################################

def _orig():
    # original -- i.e., before revision linking -- saros db state as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 3), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 3), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 3), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 0), ('last', 6), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _expected():
    # expected saros db state, after revision linking, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 8), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 8), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 8), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 8), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 8), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 6), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 7), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 7), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 7), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 7), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 4), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _rev_not_positive():
    # saros db state when rev <= 0, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', -1), ('prev', 0), ('last', 3), ('content', 'i am JE00-1')]", ###
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 3), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 3), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 0), ('last', 6), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _last_not_positive():
    # saros db state when last <= 0, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 3), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', -10), ('content', 'i am JE00-2')]", ###
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 3), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 0), ('last', 6), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _last_below_rev():
    # saros db state when last < rev, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 3), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 3), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 1), ('content', 'i am JE00-3')]", ###
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 0), ('last', 6), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _duplicate():
    # saros db state with duplicate revisions, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 8), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 8), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 8), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 8), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 8), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 6), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]", #
        "JE02-5: [('name', 'JE02'), ('rev', 4), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]", ###
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _dec_last():
    # saros db state when plast < last -- i.e., decreasing last -- as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 8), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 8), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 8), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 8), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 8), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 6), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 7), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 7), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 7), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 7), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 4), ('last', 7), ('content', 'i am JE02-5')]", ###
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE02-6')]", #
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _non_consec():
    # saros db state when revisions are not consecutive, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 6), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 6), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 6), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 6), ('content', 'i am JE00-4')]", #
        "JE00-5: [('name', 'JE00'), ('rev', 7), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]", ###
        "JE00-6: [('name', 'JE00'), ('rev', 8), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]", ###
        "JE00-7: [('name', 'JE00'), ('rev', 6), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]", ###
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _prev_missing():
    # saros db state when previous revisions are missing, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 5), ('content', 'i am JE00-1')]", ###
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 5), ('content', 'i am JE00-2')]", ###
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 5), ('content', 'i am JE00-3')]", ###
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 0), ('last', 6), ('content', 'i am JE00-4')]", #
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 6), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 6), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 0), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 4), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 4), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 4), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 4), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 0), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]",
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])

def _end_missing():
    # saros db state when end revisions are missing, as a string.
    return '\n'.join([
        "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE00-1')]",
        "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 8), ('content', 'i am JE00-2')]",
        "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 8), ('content', 'i am JE00-3')]",
        "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 8), ('content', 'i am JE00-4')]",
        "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 8), ('content', 'i am JE00-5')]",
        "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 8), ('content', 'i am JE00-6')]",
        "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 6), ('last', 8), ('content', 'i am JE00-7')]",
        "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
        "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
        "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
        "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 7), ('content', 'i am JE02-1')]",
        "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 7), ('content', 'i am JE02-2')]",
        "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 7), ('content', 'i am JE02-3')]",
        "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 7), ('content', 'i am JE02-4')]",
        "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 4), ('last', 7), ('content', 'i am JE02-5')]",
        "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
        "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
        "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE03-1')]", ###
        "JE04-1: [('name', 'JE04'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE04-1')]",
        "JE04-2: [('name', 'JE04'), ('rev', 2), ('prev', 0), ('last', 2), ('content', 'i am JE04-2')]"
    ])




