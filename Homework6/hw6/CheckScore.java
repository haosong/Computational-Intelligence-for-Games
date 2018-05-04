import java.util.Scanner;

public class CheckScore
{
    public static void main(String[] args)
    {
	double threshold = 0.0;
	try
	    {
		threshold = Double.parseDouble(args[0]);
	    }
	catch (Exception ex)
	    {
		System.out.println("FAIL -- can't read threshold argument");
		System.exit(1);
	    }
	
	Scanner in = new Scanner(System.in);
	if (!in.hasNextDouble())
	    {
		System.out.println("FAIL -- can't read input");
		System.exit(1);
	    }
	
	double score = in.nextDouble();
	System.out.println(score >= threshold ? "PASS" : "FAIL -- score " + score);    
    }
}
