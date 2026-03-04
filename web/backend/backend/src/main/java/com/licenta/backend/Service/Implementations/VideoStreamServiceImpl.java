package com.licenta.backend.Service.Implementations;

import com.licenta.backend.Model.VideoStream;
import com.licenta.backend.Repository.VideoStreamRepository;
import com.licenta.backend.Service.VideoStreamService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
@RequiredArgsConstructor
public class VideoStreamServiceImpl implements VideoStreamService {
    private final VideoStreamRepository videoStreamRepository;

    @Override
    public VideoStream saveVideoMetadata(String filename, String filePath, String uploaderId, String roadSegment) {
        VideoStream videoStream = new VideoStream();
        videoStream.setFilename(filename);
        videoStream.setFilepath(filePath);
        videoStream.setUploaderId(uploaderId);
        videoStream.setRoadSegment(roadSegment);

        return  videoStreamRepository.save(videoStream);
    }

    @Override
    public List<VideoStream> getAllVideos() {
        return videoStreamRepository.findAll();
    }

    @Override
    public List<VideoStream> getUnprocessedVideos() {
        return videoStreamRepository.findByIsProcessedFalse();
    }
}
