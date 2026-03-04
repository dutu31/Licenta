package com.licenta.backend.Repository;

import com.licenta.backend.Model.VideoStream;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface VideoStreamRepository extends JpaRepository<VideoStream, Long> {
    List<VideoStream> findByIsProcessedFalse();  //to find videos that are gonna be processed in point cloud
    List<VideoStream> findByRoadSegment(String roadSegment);
}
