---
source_id: S002
title: Ultralytics YOLO26 docs
source_url: https://docs.ultralytics.com/models/yolo26
source_file: docs/research/papers/S002-ultralytics-yolo26-docs.html
source_kind: html
extraction_note: saved source page HTML; PDF not openly downloadable by script
---

# Extracted text: S002-ultralytics-yolo26-docs.html

Source URL: https://docs.ultralytics.com/models/yolo26

Ultralytics YOLO26 | Ultralytics Docs 
 
 Meet YOLO26: next-gen vision AI. the next generation of real-time vision AI. 
 Skip to main content Ultralytics 

 Search... 
 Home 
 Quickstart 

 Home Quickstart 
 Usage 

 YOLO26 🚀 

 Modes 

 Tasks 

 Models YOLOv3 
 YOLOv4 
 YOLOv5 
 YOLOv6 
 YOLOv7 
 YOLOv8 
 YOLOv9 
 YOLOv10 
 YOLO11 
 YOLO12 
 YOLO26 🚀 
 SAM (Segment Anything Model) 
 SAM 2 (Segment Anything Model 2) 
 SAM 3 (Segment Anything Model 3) 
 MobileSAM (Mobile Segment Anything Model) 
 FastSAM (Fast Segment Anything Model) 
 YOLO-NAS (Neural Architecture Search) 
 RT-DETR (Realtime Detection Transformer) 
 YOLO-World (Real-Time Open-Vocabulary Object Detection) 
 YOLOE (Real-Time Seeing Anything) 

 Compare 

 Datasets 

 Solutions 

 Guides 

 Integrations 

 Platform 

 Reference 

 Help 

 Loading Please wait 

 Toggle Sidebar 
 Docs 
 
 Models 
 
 YOLO26 🚀 
 
 Select language GitHub 130.0k Switch apps Toggle theme 

 Ultralytics YOLO26

 Overview

 Ultralytics YOLO26 is the latest evolution in the YOLO series of real-time object detectors, engineered from the ground up for edge and low-power devices . It introduces a streamlined design that removes unnecessary complexity while integrating targeted innovations to deliver faster, lighter, and more accessible deployment.

 Try on Ultralytics Platform 
 Explore and run YOLO26 models directly on Ultralytics Platform .

 The architecture of YOLO26 is guided by three core principles:

 Simplicity: YOLO26 is a native end-to-end model , producing predictions directly without the need for non-maximum suppression (NMS). By eliminating this post-processing step, inference becomes faster, lighter, and easier to deploy in real-world systems. This breakthrough approach was first pioneered in YOLOv10 by Ao Wang at Tsinghua University and has been further advanced in YOLO26.

 Deployment Efficiency: The end-to-end design cuts out an entire stage of the pipeline, dramatically simplifying integration, reducing latency, and making deployment more robust across diverse environments.

 Training Innovation: YOLO26 introduces the MuSGD optimizer , a hybrid of SGD and Muon — inspired by Moonshot AI's Kimi K2 breakthroughs in LLM training. This optimizer brings enhanced stability and faster convergence, transferring optimization advances from language models into computer vision.

 Task-Specific Optimizations: YOLO26 introduces targeted improvements for specialized tasks, including semantic segmentation loss and multi-scale proto modules for Segmentation , Residual Log-Likelihood Estimation (RLE) for high-precision Pose estimation, and optimized decoding with angle loss to resolve boundary issues in OBB .

 Together, these innovations deliver a model family that achieves higher accuracy on small objects, provides seamless deployment, and runs up to 43% faster on CPUs — making YOLO26 one of the most practical and deployable YOLO models to date for resource-constrained environments.

 Key Features

 DFL Removal 

The Distribution Focal Loss (DFL) module, while effective, often complicated export and limited hardware compatibility. YOLO26 removes DFL entirely, simplifying inference and broadening support for edge and low-power devices .

 End-to-End NMS-Free Inference 

Unlike traditional detectors that rely on NMS as a separate post-processing step, YOLO26 is natively end-to-end . Predictions are generated directly, reducing latency and making integration into production systems faster, lighter, and more reliable.

 ProgLoss + STAL 

Improved loss functions increase detection accuracy, with notable improvements in small-object recognition , a critical requirement for IoT, robotics, aerial imagery, and other edge applications.

 MuSGD Optimizer 

A new hybrid optimizer that combines SGD with Muon . Inspired by Moonshot AI's Kimi K2 , MuSGD introduces advanced optimization methods from LLM training into computer vision, enabling more stable training and faster convergence.

 Up to 43% Faster CPU Inference 

Specifically optimized for edge computing, YOLO26 delivers significantly faster CPU inference, ensuring real-time performance on devices without GPUs.

 Instance Segmentation Enhancements 

Introduces semantic segmentation loss to improve model convergence and an upgraded proto module that leverages multi-scale information for superior mask quality.

 Precision Pose Estimation 

Integrates Residual Log-Likelihood Estimation (RLE) for more accurate keypoint localization and optimizes the decoding process for increased inference speed.

 Refined OBB Decoding 

Introduces a specialized angle loss to improve detection accuracy for square-shaped objects and optimizes OBB decoding to resolve boundary discontinuity issues.

 Supported Tasks and Modes

 YOLO26 builds upon the versatile model range established by earlier Ultralytics YOLO releases, offering enhanced support across various computer vision tasks:

 Model Filenames Task Inference Validation Training Export 
 YOLO26 yolo26n.pt yolo26s.pt yolo26m.pt yolo26l.pt yolo26x.pt Detection ✅ ✅ ✅ ✅ 
 YOLO26-seg yolo26n-seg.pt yolo26s-seg.pt yolo26m-seg.pt yolo26l-seg.pt yolo26x-seg.pt Instance Segmentation ✅ ✅ ✅ ✅ 
 YOLO26-sem yolo26n-sem.pt yolo26s-sem.pt yolo26m-sem.pt yolo26l-sem.pt yolo26x-sem.pt Semantic Segmentation ✅ ✅ ✅ ✅ 
 YOLO26-pose yolo26n-pose.pt yolo26s-pose.pt yolo26m-pose.pt yolo26l-pose.pt yolo26x-pose.pt Pose/Keypoints ✅ ✅ ✅ ✅ 
 YOLO26-obb yolo26n-obb.pt yolo26s-obb.pt yolo26m-obb.pt yolo26l-obb.pt yolo26x-obb.pt Oriented Detection ✅ ✅ ✅ ✅ 
 YOLO26-cls yolo26n-cls.pt yolo26s-cls.pt yolo26m-cls.pt yolo26l-cls.pt yolo26x-cls.pt Classification ✅ ✅ ✅ ✅ 

 This unified framework ensures YOLO26 is applicable across real-time detection, instance segmentation, semantic segmentation, classification, pose estimation, and oriented object detection — all with training, validation, inference, and export support.
 Architecture-only variants 
 yolo26-p2.yaml and yolo26-p6.yaml add a P2 (small-object) or P6 (large-input) detection head and are shipped as YAML architectures only. No scale-specific yolo26*-p2.pt or yolo26*-p6.pt weights are released. Instantiate a scaled config from YAML (for example, YOLO("yolo26n-p6.yaml") ) and train or fine-tune it as needed.

 Performance Metrics
 Performance 
 Detection (COCO) Segmentation (COCO) Semantic Segmentation (Cityscapes) Classification (ImageNet) Pose (COCO) OBB (DOTAv1) 
 See Detection Docs for usage examples with these models trained on COCO , which include 80 pretrained classes.

 Model size
 (pixels) mAP val
50-95 mAP val
50-95(e2e) Speed
 CPU ONNX
(ms) Speed
 T4 TensorRT10
(ms) params
 (M) FLOPs
 (B) 
 YOLO26n 640 40.9 40.1 38.9 ± 0.7 1.7 ± 0.0 2.4 5.4 
 YOLO26s 640 48.6 47.8 87.2 ± 0.9 2.5 ± 0.0 9.5 20.7 
 YOLO26m 640 53.1 52.5 220.0 ± 1.4 4.7 ± 0.1 20.4 68.2 
 YOLO26l 640 55.0 54.4 286.2 ± 2.0 6.2 ± 0.2 24.8 86.4 
 YOLO26x 640 57.5 56.9 525.8 ± 4.0 11.8 ± 0.2 55.7 193.9 

 Params and FLOPs values are for the fused model after model.fuse() , which merges Conv and BatchNorm layers and removes the auxiliary one-to-many detection head. Pretrained checkpoints retain the full training architecture and may show higher counts. 

 Usage Examples

 This section provides simple YOLO26 training and inference examples. For full documentation on these and other modes , see the Predict , Train , Val , and Export docs pages.

 Note that the example below is for YOLO26 Detect models for object detection . For additional supported tasks, see the Segment , Semantic Segmentation , Classify , OBB , and Pose docs.
 Example 
 Python CLI 
 PyTorch pretrained *.pt models as well as configuration *.yaml files can be passed to the YOLO() class to create a model instance in Python:

 from ultralytics import YOLO

 # Load a COCO-pretrained YOLO26n model 
model = YOLO( "yolo26n.pt" )

 # Train the model on the COCO8 example dataset for 100 epochs 
results = model.train(data= "coco8.yaml" , epochs= 100 , imgsz= 640 )

 # Run inference with the YOLO26n model on the 'bus.jpg' image 
results = model( "path/to/bus.jpg" ) 

 Dual-Head Architecture 
 YOLO26 features a dual-head architecture that provides flexibility for different deployment scenarios:

 One-to-One Head (Default) : Produces end-to-end predictions without NMS, outputting (N, 300, 6) with a maximum of 300 detections per image. This head is optimized for fast inference and simplified deployment.

 One-to-Many Head : Generates traditional YOLO outputs requiring NMS post-processing, outputting (N, nc + 4, 8400) where nc is the number of classes. This head typically achieves slightly higher accuracy at the cost of additional processing.

 You can switch between heads during export, prediction, or validation:
 Python CLI 
 from ultralytics import YOLO

model = YOLO( "yolo26n.pt" )

 # Use one-to-one head (default, no NMS required) 
results = model.predict( "image.jpg" ) # inference 
metrics = model.val(data= "coco.yaml" ) # validation 
model.export( format = "onnx" ) # export 

 # Use one-to-many head (requires NMS) 
results = model.predict( "image.jpg" , end2end= False ) # inference 
metrics = model.val(data= "coco.yaml" , end2end= False ) # validation 
model.export( format = "onnx" , end2end= False ) # export 

 The choice depends on your deployment requirements: use the one-to-one head for maximum speed and simplicity, or the one-to-many head when accuracy is the top priority.

 YOLOE-26: Open-Vocabulary Instance Segmentation

 YOLOE-26 integrates the high-performance YOLO26 architecture with the open-vocabulary capabilities of the YOLOE series. It enables real-time detection and segmentation of any object class using text prompts , visual prompts , or a prompt-free mode for zero-shot inference, effectively removing the constraints of fixed-category training.

 By leveraging YOLO26's NMS-free, end-to-end design , YOLOE-26 delivers fast open-world inference. This makes it a powerful solution for edge applications in dynamic environments where the objects of interest represent a broad and evolving vocabulary.
 Performance 
 Text/Visual Prompts Prompt-free 
 See YOLOE Docs for usage examples with these models trained on Objects365v1 , GQA and Flickr30k datasets.

 Model size
 (pixels) Prompt Type mAP minival
50-95(e2e) mAP minival
50-95 mAP r mAP c mAP f params
 (M) FLOPs
 (B) 
 YOLOE-26n-seg 640 Text/Visual 23.7 / 20.9 24.7 / 21.9 20.5 / 17.6 24.1 / 22.3 26.1 / 22.4 4.8 6.0 
 YOLOE-26s-seg 640 Text/Visual 29.9 / 27.1 30.8 / 28.6 23.9 / 25.1 29.6 / 27.8 33.0 / 29.9 13.1 21.7 
 YOLOE-26m-seg 640 Text/Visual 35.4 / 31.3 35.4 / 33.9 31.1 / 33.4 34.7 / 34.0 36.9 / 33.8 27.9 70.1 
 YOLOE-26l-seg 640 Text/Visual 36.8 / 33.7 37.8 / 36.3 35.1 / 37.6 37.6 / 36.2 38.5 / 36.1 32.3 88.3 
 YOLOE-26x-seg 640 Text/Visual 39.5 / 36.2 40.6 / 38.5 37.4 / 35.3 40.9 / 38.8 41.0 / 38.8 69.9 196.7 

 Usage Example

 YOLOE-26 supports both text-based and visual prompting. Using prompts is straightforward—just pass them through the predict method as shown below:
 Example 
 Text Prompt Visual Prompt Prompt free 
 Text prompts allow you to specify the classes that you wish to detect through textual descriptions. The following code shows how you can use YOLOE-26 to detect people and buses in an image:

 from ultralytics import YOLO

 # Initialize model 
model = YOLO( "yoloe-26l-seg.pt" ) # or select yoloe-26s/m-seg.pt for different sizes 

 # Set text prompt to detect person and bus. You only need to do this once after you load the model. 
model.set_classes([ "person" , "bus" ])

 # Run detection on the given image 
results = model.predict( "path/to/image.jpg" )

 # Show results 
results[ 0 ].show() 

 For a deep dive into prompting techniques, training from scratch, and full usage examples, visit the YOLOE Documentation .

 Citations and Acknowledgments
 Ultralytics YOLO26 Publication 
 Ultralytics has not published a formal research paper for YOLO26 due to the rapidly evolving nature of the models. Instead, we focus on delivering cutting-edge models and making them easy to use. For the latest updates on YOLO features, architectures, and usage, visit our GitHub repository and documentation .

 If you use YOLO26 or other Ultralytics software in your work, please cite it as:
 Quote 
 BibTeX 
 @software{yolo26_ultralytics,
 author = {Glenn Jocher and Jing Qiu},
 title = {Ultralytics YOLO26},
 version = {26.0.0},
 year = {2026},
 url = {https://github.com/ultralytics/ultralytics},
 orcid = {0000-0001-5950-6979, 0000-0003-3783-7069},
 license = {AGPL-3.0}
} 

 DOI pending. YOLO26 is available under AGPL-3.0 and Enterprise licenses.

 FAQ

 What are the key improvements in YOLO26 compared to YOLO11?

 DFL Removal : Simplifies export and expands edge compatibility

 End-to-End NMS-Free Inference : Eliminates NMS for faster, simpler deployment

 ProgLoss + STAL : Boosts accuracy, especially on small objects

 MuSGD Optimizer : Combines SGD and Muon (inspired by Moonshot's Kimi K2) for more stable, efficient training

 Up to 43% Faster CPU Inference : Major performance gains for CPU-only devices

 What tasks does YOLO26 support?

 YOLO26 is a unified model family , providing end-to-end support for multiple computer vision tasks:

 Object Detection 

 Instance Segmentation 

 Semantic Segmentation 

 Image Classification 

 Pose Estimation 

 Oriented Object Detection (OBB) 

 Each size variant (n, s, m, l, x) supports all tasks, plus open-vocabulary versions via YOLOE-26 .

 Why is YOLO26 optimized for edge deployment?

 YOLO26 delivers state-of-the-art edge performance with:

 Up to 43% faster CPU inference

 Reduced model size and memory footprint

 Architecture simplified for compatibility (no DFL, no NMS)

 Flexible export formats including TensorRT, ONNX, CoreML, TFLite, and OpenVINO

 How do I get started with YOLO26?

 YOLO26 models were released on January 14, 2026, and are available for download. Install or update the ultralytics package and load a model:

 from ultralytics import YOLO

 # Load a pretrained YOLO26 nano model 
model = YOLO( "yolo26n.pt" )

 # Run inference on an image 
results = model( "image.jpg" ) 

 See the Usage Examples section for training, validation, and export instructions.

 Contributors
 
 GL glenn-jocher 6 LA Laughing-q 5 RA raimbekovm 3 Y- Y-T-G 3 FC fcakyon 1 LM lmycross 1 PD pderrenger 1 

 Created Sep 25, 2025 Updated 5 days ago 

 Comments

 On This Page
 Overview Key Features Supported Tasks and Modes Performance Metrics Usage Examples YOLOE-26: Open-Vocabulary Instance Segmentation Usage Example Citations and Acknowledgments FAQ What are the key improvements in YOLO26 compared to YOLO11? What tasks does YOLO26 support? Why is YOLO26 optimized for edge deployment? How do I get started with YOLO26? 
 
 Previous
 Advanced Customization

 Next
 Ultralytics YOLO26 Modes