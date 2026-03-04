package com.licenta.backend.Service;

import com.licenta.backend.Model.VideoStream;

import java.util.List;

public interface VideoStreamService {
    VideoStream saveVideoMetadata(String filename, String filePath, String uploaderId, String roadSegment);
    List<VideoStream> getAllVideos();
    List<VideoStream>getUnprocessedVideos();
}
