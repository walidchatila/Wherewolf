package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class GameAdapter extends ArrayAdapter<Games>{
	 public GameAdapter(Context context, ArrayList<Games> games) {
	        super(context, 0, games);
	     }
	 
	 @Override
	 public View getView(int position, View convertView, ViewGroup parent){
		 Games games = getItem(position);
		 if (convertView == null){
			 convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_game, parent, false);
		 }
		 TextView game_id = (TextView) convertView.findViewById(R.id.description);
		 TextView game_name = (TextView) convertView.findViewById(R.id.game_name);
		 
		 game_id.setText(games.getDescription());
		 game_name.setText(games.getName());
		 
		 return convertView;
	 }
}

