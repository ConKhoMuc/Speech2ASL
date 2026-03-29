package vn.iotstar.appspeech2asl;

import java.util.List;

public class VideoResponse {

    private String text;
    private List<String> nlptext;
    private String video;
    private boolean cached;

    public String getText() {
        return text;
    }

    public List<String> getNlptext() {
        return nlptext;
    }

    public String getVideo() {
        return video;
    }

    public boolean isCached() {
        return cached;
    }
}