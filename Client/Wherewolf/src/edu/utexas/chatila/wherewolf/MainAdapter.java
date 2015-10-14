package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class MainAdapter extends ArrayAdapter<Players>{
	 public MainAdapter(Context context, ArrayList<Players> players) {
	        super(context, 0, players);
	     }
	 
	 @Override
	 public View getView(int position, View convertView, ViewGroup parent){
		 Players players = getItem(position);
		 if (convertView == null){
			 convertView = LayoutInflater.from(getContext()).inflate(R.layout.playermain, parent, false);
		 }
		 ImageView profile_pic = (ImageView) convertView.findViewById(R.id.profilepic);
		 TextView game_name = (TextView) convertView.findViewById(R.id.Name);
		// TextView num_votes = (TextView) convertView.findViewById(R.id.Votes);

		 if (players.getProfilepic().equals("male")){
				profile_pic.setImageResource(R.drawable.villager3);		}
		 
		 if (players.getProfilepic().equals("female")){
		profile_pic.setImageResource(R.drawable.villager1);
		}
		
		game_name.setText(players.getName());
		//num_votes.setText(players.getNumvotes());

		 
	    return convertView;
	 }
}


