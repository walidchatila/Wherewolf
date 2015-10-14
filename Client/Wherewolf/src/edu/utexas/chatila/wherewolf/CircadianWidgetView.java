package edu.utexas.chatila.wherewolf;

import java.util.jar.Attributes;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class CircadianWidgetView extends View {
	
	public CircadianWidgetView(Context context, AttributeSet attrs){
		super(context, attrs);
		initPaint();

	}
	
	private Paint canvasPaint, drawPaint;
	private Bitmap canvasBitmap, moonBitmap, sunBitmap, nightBitmap, dayBitmap, dusk1Bitmap, dusk2Bitmap;
	private Canvas drawCanvas;
	double currentTime;
	private  Paint dayPaint;  

	private void initPaint(){
		drawPaint = new Paint();
		canvasPaint = new Paint(Paint.DITHER_FLAG);
		moonBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.moon);
		nightBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.night);
		sunBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.sun);
		dayBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.day);
		dusk1Bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.dusk1);
		dusk2Bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.dusk2);
		dayPaint = new Paint(); 
		dayPaint.setAlpha(128);
		
	}
		
	public void changeTime(double time){
		currentTime = time;
		
		invalidate();
	}
	
	protected void onDraw(Canvas canvas){
		double w = drawCanvas.getWidth();
		double h = drawCanvas.getHeight();
		
		int iW = moonBitmap.getWidth() / 2; 
		int iH = moonBitmap.getHeight() / 2;
		
		// draw the backdrop here
		
		if( currentTime < 12)
		{dayPaint.setAlpha((int)(currentTime/12 * 255));
		}
		else{
			dayPaint.setAlpha((int)(((24 -currentTime)/12)*255));
		}
			drawCanvas.drawBitmap(nightBitmap,0, 0, drawPaint);
			drawCanvas.drawBitmap(dayBitmap,0, 0, dayPaint);
		// drawCanvas.drawBitmap(dusk1Bitmap,0, 0, drawPaint);
		// drawCanvas.drawBitmap(dusk2Bitmap,0, 0, drawPaint);
		
		// calculate the angle the moon should appear in the sky
		double theta = Math.PI / 2 + Math.PI * currentTime / 12;

		// calculate the x and y coordinates of where to draw the images
		// keep in mind the coordinates are the top left of the images
		// so you can use the bitmap width and height to compensate.

		double moonPosX = w / 2 - w / 3 * -Math.cos(theta);
	    double moonPosY = (h + 2*iH) / 2 - h / 2 * -(Math.sin(-theta - 2*(Math.PI)) ); // replace this with your value

	    double sunPosX = w / 2 - w / 3 * Math.cos(theta);
	    double sunPosY = (h + 2*iH) / 2 - h / 2 * (Math.sin(-theta - 2*(Math.PI) ));
	    
	    drawCanvas.drawBitmap(moonBitmap, 
	    (int) moonPosX - iW, (int) moonPosY + iH, drawPaint); 

	    drawCanvas.drawBitmap(sunBitmap, 
	    	   (int) sunPosX - iW, (int) sunPosY + iH, drawPaint);
		// draw your sun and other things here as well.
		// experiment with drawCanvas.drawText for putting labels of whether it is day
		// or night.

		// you need to actually move the offscreen bitmap to the on-screen bitmap
		canvas.drawBitmap(canvasBitmap, 0, 0, drawPaint);

	}
	
	@Override
	protected void onSizeChanged(int w, int h, int oldw, int oldh) {
		super.onSizeChanged(w, h, oldw, oldh);

		canvasBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
		drawCanvas = new Canvas(canvasBitmap);
	}}
	
	