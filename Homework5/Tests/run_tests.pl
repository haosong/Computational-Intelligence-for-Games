&sectionHeader('MCTS');
@SOURCE = ();
@LINK = ('/c/cs474/hw5/Tests/kalah.py', '/c/cs474/hw5/Tests/minimax.py', '/c/cs474/hw5/Tests/test_mcts.py');
$subtotal = &runTest('001', '1000 iterations');
$total += floor($subtotal);
&sectionResults('MCTS', $subtotal);

