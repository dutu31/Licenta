package com.licenta.backend.Model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
@Entity
@Table(name = "video_streams")
@Data //lombok
@NoArgsConstructor
public class VideoStream {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        @Column(nullable = false)
        private String filename;
        @Column(nullable = false)
        private String filepath;
        @Column(nullable = false)
        private String uploaderId;
        @Column(nullable = false)
        private String roadSegment;    //name of the location
        @Column(name="uploaded_at")
        private LocalDateTime uploadedAt;
        @Column(name="is_processed")
        private Boolean isProcessed; //if it was included in the cloud point
        @PrePersist
        protected void onCreate() {
            this.uploadedAt = LocalDateTime.now();
            this.isProcessed = false;
        }
    }

