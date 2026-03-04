package com.licenta.backend.Facades.Implementations;

import com.licenta.backend.Converter.VideoStreamConverter;
import com.licenta.backend.Facades.VideoStreamFacade;
import com.licenta.backend.Model.VideoStream;
import com.licenta.backend.Service.FileStorageService;
import com.licenta.backend.Service.VideoStreamService;
import com.licenta.backend.dto.VideoStreamResponseDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class VideoStreamFacadeImpl implements VideoStreamFacade {
    private final VideoStreamService videoStreamService;
    private final VideoStreamConverter videoStreamConverter;
    private final FileStorageService fileStorageService;

    @Override
    public VideoStreamResponseDTO processAndSaveVideo(MultipartFile file, String uploaderId, String roadSegment) throws IOException {
        //TO DO: Saving file on disk
        String savedFilePath=fileStorageService.saveVideoFile(file);
        String originalFilename=file.getOriginalFilename();

        //2.Saving data to db
        VideoStream savedVideo=videoStreamService.saveVideoMetadata(
                originalFilename,savedFilePath,uploaderId,roadSegment
        );
        //TO DO: Send notification to 3d processing system
        return videoStreamConverter.toDTO(savedVideo);
    }

    @Override
    public List<VideoStreamResponseDTO> getAllVideos() {
        return videoStreamService.getAllVideos()
                .stream()
                .map(videoStreamConverter::toDTO)
                .collect(Collectors.toList());
    }
}
