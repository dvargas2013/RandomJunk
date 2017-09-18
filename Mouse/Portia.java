import java.awt.MouseInfo;
import java.awt.Point;
import java.util.Scanner;

public class Portia {
	public static void main(String[] args) {
		Point spot;
		Scanner in = new Scanner(System.in);
		String input = "";
		while (input.length() < 1) {
			spot = MouseInfo.getPointerInfo().getLocation();
			System.out.println(""+(int) spot.getX()+" "+(int) spot.getY());
			input = in.nextLine();
		}
	}
}