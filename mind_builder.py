

class MindBuilder(object):

    def __init__(self, gene):

        self.gene = gene

    # Run a neural network over the gene, producing a neural network.
    def make_mind(self):

        # Start with a single node, and a decoder.
        # Decoder comes from previous generations.
        # Run the decoder over the gene.
        # Decoder must decide to halt, divide, or specialize.
        # 