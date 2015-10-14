package edu.utexas.chatila.wherewolf;

import android.util.Log;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;


public class MyOnChangeListener implements OnSeekBarChangeListener {
	private CircadianWidgetView myCircadianwidget;
	
	private static final String TAG = "Listener";

	public void setCircadianWidget(CircadianWidgetView c){
		this.myCircadianwidget = c;
	}
	
	@Override
	public void onProgressChanged(SeekBar seekBar, int progress,
			boolean fromUser) {
		//seekBar.setProgress(0);
		seekBar.setMax(24);
		myCircadianwidget.changeTime(progress);
		Log.v(TAG, "currenttime " + myCircadianwidget.currentTime);
	
		

		// TODO Auto-generated method stub
		
	}
	@Override
	public void onStartTrackingTouch(SeekBar seekBar) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void onStopTrackingTouch(SeekBar seekBar) {
		// TODO Auto-generated method stub
		
	}
	
}
