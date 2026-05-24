import java.util.LinkedList;

import java.util.*;

    class Graph {

        // Add edge
        static void addEdge(LinkedList<ArrayList<Integer>> am, int s, int d) {
            am.get(s).add(d);
            am.get(d).add(s);
        }

       public static LinkedList<ArrayList<Integer>> generateEdges(){

            // Create the graph
            int V = 5;
            LinkedList<ArrayList<Integer>> am = new LinkedList<ArrayList<Integer>>();

            for (int i = 0; i < V; i++)
                am.add(new ArrayList<Integer>());

            // Add edges
            addEdge(am, 0, 1);
            addEdge(am, 0, 2);
            addEdge(am, 0, 3);
            addEdge(am, 1, 2);

           return am;
        }

        // Print the graph
        static void printGraph(LinkedList<ArrayList<Integer>> am) {
            for (int i = 0; i < am.size(); i++) {
                System.out.println("\nVertex " + i + ":");
                for (int j = 0; j < am.get(i).size(); j++) {
                    System.out.print(" -> " + am.get(i).get(j));
                }
                System.out.println();
            }
        }
    }

