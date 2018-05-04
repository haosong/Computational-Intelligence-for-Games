&sectionHeader('Basic Threshold');
@SOURCE = ();
@LINK = ('/c/cs474/hw6/Tests/test_yahtzee.py', '/c/cs474/hw6/Tests/yahtzee.py');
$subtotal = &runTest('001', '190 points');
$subtotal = $subtotal * 50 / 1;
$total += floor($subtotal);
&sectionResults('Basic Threshold', $subtotal);

&sectionHeader('Five Points Each');
@SOURCE = ();
@LINK = ('/c/cs474/hw6/Tests/test_yahtzee.py', '/c/cs474/hw6/Tests/yahtzee.py');
$subtotal = &runTest('002', '195 points');
$subtotal += &runTest('003', '200 points');
$subtotal += &runTest('004', '205 points');
$subtotal += &runTest('005', '210 points');
$subtotal += &runTest('006', '215 points');
$subtotal += &runTest('007', '220 points');
$subtotal += &runTest('008', '230 points');
$subtotal += &runTest('009', '236 points');
$total += floor($subtotal);
&sectionResults('Five Points Each', $subtotal);

&sectionHeader('One point each');
@SOURCE = ();
@LINK = ('/c/cs474/hw6/Tests/test_yahtzee.py', '/c/cs474/hw6/Tests/yahtzee.py');
$subtotal = &runTest('010', '238 points');
$subtotal += &runTest('011', '240 points');
$subtotal += &runTest('012', '242 points');
$subtotal += &runTest('013', '244 points');
$subtotal += &runTest('014', '245 points');
$subtotal += &runTest('015', '246 points');
$subtotal += &runTest('016', '247 points');
$subtotal += &runTest('017', '248 points');
$subtotal += &runTest('018', '249 points');
$subtotal += &runTest('019', '250 points');
$total += floor($subtotal);
&sectionResults('One point each', $subtotal);

