# -*- coding: utf-8 -*-
'''
    finance.ofx.parse
    ~~~~~~~~~~~~~~~~

    A small utility for parsing ofx data grams.

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''

class Tree():
    ''' Tree provides a tree representation of an OFX datagram. '''

    def __init__(self, strgram):
        ''' Tree initialization objects
        strgram: Original string representation of the ofx datagram.
        nodes: A list of all the nodes, tags and fields from the datagram.
        tree: A list of the locations of all opentags, in order.
        '''
        self.strgram = strgram
        datagram = DatagramIter(strgram)
        self.nodes = []
        self.tree = []
        self._buildtree(datagram)

    def _maketagnode(self, element):
        ''' Used to extract tag values returns a Node object. '''
        if self._isclosetag(element):
            etype = 'closetag'
        else:
            etype = 'opentag'
        key = element.strip('<>/')
        return Node(etype = etype, key = key)

    def _makefieldnode(self, element):
        ''' used to extract field values and returns a Node object. '''
        etype = 'field'
        div = element.split('>')
        key = div[0].strip('<')
        value = div[1]
        return Node(etype = etype, key = key, value = value)

    def _field2opentag(self, node):
        node.etype = 'opentag'
        node.value = ''
        return node

    def _isclosetag(self, element):
        return (element.find('</') >= 0)

    def _buildtree(self, datagram):
        ''' Parses the OFX datagram string. '''
        candidates = {}
        for element in datagram:
            node = None
            if self._isclosetag(element):
                node = self._maketagnode(element)
            else:
                node = self._makefieldnode(element)
            self.nodes.append(node)
            nodeposition = len(self.nodes) - 1

            # Cache all empty field nodes as potential opentag candidates.
            if (node.etype == 'field' and len(node.value) == 0):
                if candidates.has_key(node.key):
                    candidates[node.key].append(nodeposition)
                else:
                    tmplst = []
                    tmplst.append(nodeposition)
                    candidates[node.key] = tmplst
            # If this is a close tag, check for the matching open tag
            elif node.etype == 'closetag':
                if candidates.has_key(node.key):
                    nodeposition = candidates[node.key].pop()
                    # Ensure we always get the newest matching opentag as
                    # there may be nested tags of the same name.
                    opentag = self.nodes[nodeposition]
                    opentag = self._field2opentag(opentag)

                    # All elements from opentag+1 to closetag-1 are children of this tag.
                    opentag.children = [c for c in self.nodes[nodeposition+1:]]

                    # There's no need to keep the close tags
                    self.nodes.pop()

                    # Add new opentag location to the tree list
                    self.tree.append(nodeposition)
                else:
                    return "close tag found before open tag, data is incomplete"

        # The tree has been built in reverse order since we keyed off the closetags.
        self.tree.reverse()

# - End Tree Class -------------

class Node():
    ''' Custom node class for each element in an OFX datagram.

    This class essentially wraps a tuple for:
        - The type of element (field or tag)
        - The key name of the element
        - If a field, the data held in the element
        - Otherwise, if a tag, a list of all children tags and fields
    '''

    def __init__(self, etype, key, value = ''):
        if (etype.find('tag') < 0 and etype != 'field'):
            raise ValueError
        else:
            self.etype = etype
            self.key = key
            self.value = value
            self.children = []

    def append(self, child):
        self.children.append(child)

    def show(self):
        return 'type='+self.etype+' key='+self.key+' value='+self.value

# - End Node class ---------------

class DatagramIter():
    ''' Custom container for iterating over raw OFX datagrams. '''

    def __init__(self,datagram):
        self.strgram = str(datagram)
        self.length = len(self.strgram)
        self.pos=0

    def __iter__(self):
        return self

    def next(self):
        concat = self.strgram[self.pos:]
        if self.pos >= self.length or concat.find('<') < 0:
            raise StopIteration
        else:
            start = concat.find('<')
            # only if start is not 0 we need to increase the value
            if start > 0:
                start += 1
            elif start < 0:
                raise StopIteration

            end = concat[start+1:].find('<')
            if end < 0:
                element = concat[start:]
                end = self.length
            else:
                element = concat[start:end + 1]

            self.pos = (self.pos + end + 1)
            return element

# - End DatagramIter Class -------------

Parse = Tree
