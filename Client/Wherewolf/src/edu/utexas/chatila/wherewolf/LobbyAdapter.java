package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class LobbyAdapter extends ArrayAdapter<Players> {
	 public LobbyAdapter(Context context, ArrayList<Players> players) {
	        super(context, 0, players);
	     }
	 
	private static final String TAG = "LobbyAdapter";

	 
	 @Override
	 public View getView(int position, View convertView, ViewGroup parent){
		 Players players = getItem(position);
		 if (convertView == null){
			 convertView = LayoutInflater.from(getContext()).inflate(R.layout.playerlobby, parent, false);
		 }
		 ImageView profile_pic = (ImageView) convertView.findViewById(R.id.profilepic);
		 TextView game_name = (TextView) convertView.findViewById(R.id.Name);
 
		 if (players.getProfilepic().equals("male")){
				profile_pic.setImageResource(R.drawable.villager3);		
				Log.v(TAG, players.getProfilepic());
		
		 }
		 
		 if (players.getProfilepic().equals("female")){
		profile_pic.setImageResource(R.drawable.villager1);
		Log.v(TAG, players.getProfilepic());
		}
		game_name.setText(players.getName());

		 
	    return convertView;
	 }
}



