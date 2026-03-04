package com.licenta.backend.Controller;

import com.licenta.backend.Facades.VideoStreamFacade;
import com.licenta.backend.dto.VideoStreamResponseDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/videos")
@RequiredArgsConstructor
public class VideoStreamController {

    private final VideoStreamFacade  videoStreamFacade;
    @PostMapping("/upload")
    public ResponseEntity <?> uploadVideo(
            @RequestParam("file")MultipartFile file,
            @RequestParam("uploaderId") String uploaderId,
            @RequestParam("roadSegment") String roadSegment
            )
    {
        try {
            VideoStreamResponseDTO response=videoStreamFacade.processAndSaveVideo(file,uploaderId,roadSegment);
            return ResponseEntity.ok().body(response);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error at saving file" + e.getMessage());
        }
    }

    @GetMapping
    public ResponseEntity<List<VideoStreamResponseDTO>> getAllVideos(){
        return ResponseEntity.ok(videoStreamFacade.getAllVideos());
    }
}
