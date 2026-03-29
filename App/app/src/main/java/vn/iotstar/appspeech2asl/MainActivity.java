package vn.iotstar.appspeech2asl;

import android.Manifest;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.OptIn;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.media3.common.util.UnstableApi;
import androidx.media3.datasource.DefaultHttpDataSource;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.common.MediaItem;
import androidx.media3.exoplayer.source.MediaSource;
import androidx.media3.exoplayer.source.ProgressiveMediaSource;
import androidx.media3.ui.PlayerView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.io.File;
import java.util.HashMap;
import java.util.List;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.MediaType;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.view.animation.Animation;
import android.view.animation.AnimationUtils;

public class MainActivity extends AppCompatActivity {

    private static final String BASE_URL1 = "http://192.168.2.4:8000/";
    //private static final String BASE_URL1 = "http://speechasl.iotstar.vn/";
    private Animation micPulse;
    private Animation micAlpha;
    private FloatingActionButton btnRecord;
    private ProgressBar progressBar;
    private PlayerView playerView;

    private TextView txtText;
    private TextView txtNlpText;

    private boolean isRecording = false;
    private MediaRecorder recorder;
    private File audioFile;
    private static final int REQUEST_MIC = 1;
    private ExoPlayer player;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.RECORD_AUDIO},
                    REQUEST_MIC);
        }
        if (!hasMicPermission()) {
            Toast.makeText(this, "Need microphone permission", Toast.LENGTH_SHORT).show();
            return;
        }
        //ánh xạ tên của layout
        btnRecord = findViewById(R.id.btnRecord);
        progressBar = findViewById(R.id.progressBar);
        playerView = findViewById(R.id.playerView);
         txtText = findViewById(R.id.txtText);
         txtNlpText = findViewById(R.id.txtNlpText);
        micPulse = AnimationUtils.loadAnimation(this, R.anim.mic_pulse);
        micAlpha = AnimationUtils.loadAnimation(this, R.anim.mic_alpha);


        // Init player
        player = new ExoPlayer.Builder(this).build();
        playerView.setPlayer(player);
        player.stop();
        player.clearMediaItems();
        // Ẩn controller
        //playerView.setUseController(false);
        MediaItem item = MediaItem.fromUri("");

        player.setMediaItem(item);
        player.prepare();
        player.play();

        btnRecord.setOnClickListener(v -> toggleRecording());
    }

    private boolean hasMicPermission() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_GRANTED;
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startRecording(); // 🔥 gọi lại
            }
        }
    }
    private void toggleRecording() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
            uploadAudio();
        }
        isRecording = !isRecording;
    }

    private void startRecording() {

        if (!hasMicPermission()) {
            ActivityCompat.requestPermissions(
                    this,
                    new String[]{Manifest.permission.RECORD_AUDIO},
                    REQUEST_MIC
            );
            return;
        }

        btnRecord.startAnimation(micPulse);
        btnRecord.startAnimation(micAlpha);

        audioFile = new File(getCacheDir(), "audio.mp4");

        recorder = new MediaRecorder();

        try {

            recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
            recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);

            recorder.setAudioChannels(1);
            recorder.setAudioSamplingRate(44100);
            recorder.setAudioEncodingBitRate(96000);

            recorder.setOutputFile(audioFile.getAbsolutePath());

            recorder.prepare();
            recorder.start();

        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this,
                    "Record Error: " + e.getMessage(),
                    Toast.LENGTH_LONG).show();
        }
    }

    private void stopRecording() {

        btnRecord.clearAnimation();

        try {
            if (recorder != null) {
                recorder.stop();
                recorder.reset();
                recorder.release();
                recorder = null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }



    private void uploadAudio() {
        progressBar.setVisibility(View.VISIBLE);
        uploadAudioRetrofit(audioFile);
    }

    @OptIn(markerClass = UnstableApi.class)
    private void playVideos(String videoUrls) {
        player.stop();
        player.clearMediaItems();
        String url = videoUrls + "?t=" + System.currentTimeMillis();
        DefaultHttpDataSource.Factory factory =
                new DefaultHttpDataSource.Factory()
                        .setDefaultRequestProperties(
                                new HashMap<String, String>() {{
                                    put("Cache-Control", "no-cache");
                                }}
                        );
        MediaSource mediaSource =
                new ProgressiveMediaSource.Factory(factory)
                        .createMediaSource(MediaItem.fromUri(url));
        player.setMediaSource(mediaSource);
        // Ẩn controller
        //playerView.setUseController(false);
        player.prepare();
        player.play();
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (player != null) {
            player.release();
        }
    }

    private void uploadAudioRetrofit(File file) {

        ApiService api =
                RetrofitClient.getInstance().create(ApiService.class);

        RequestBody requestFile =
                RequestBody.create(
                        MediaType.parse("audio/*"),
                        file
                );

        MultipartBody.Part body =
                MultipartBody.Part.createFormData(
                        "audio",
                        file.getName(),
                        requestFile
                );

        Call<VideoResponse> call = api.uploadAudio(body);

        call.enqueue(new Callback<VideoResponse>() {

            @Override
            public void onResponse(
                    Call<VideoResponse> call,
                    Response<VideoResponse> response
            ) {

                if (response.isSuccessful() && response.body() != null) {

                    VideoResponse body = response.body();

                    String videoUrl = body.getVideo();
                    String text = body.getText();
                    List<String> dword = body.getNlptext();
                    Log.d("LIST", String.valueOf(dword));
                    runOnUiThread(() -> {

                        progressBar.setVisibility(View.GONE);

                        txtText.setText(text);

                        if (dword != null && !dword.isEmpty()) {
                            txtNlpText.setText(TextUtils.join(", ", dword));
                        }

                        playVideos(BASE_URL1 + videoUrl);
                    });

                    }
            }

            @Override
            public void onFailure(
                    Call<VideoResponse> call,
                    Throwable t
            ) {
                Log.e("SERVER_ERROR", t.toString());
                runOnUiThread(() -> {
                    progressBar.setVisibility(View.GONE);
                    Toast.makeText(MainActivity.this,
                            "Server Error", Toast.LENGTH_SHORT).show();
                });

                Log.e("API", t.getMessage());
            }
        });
    }

}