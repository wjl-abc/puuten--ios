//
//  ImageViewCell.h
//  WaterFlowViewDemo
//
//  Created by Smallsmall on 12-6-12.
//  Copyright (c) 2012年 activation group. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import "WaterFlowViewCell.h"
#import "UIImageView+WebCache.h"

@class ImageViewCell;
@protocol ImageViewCellDelegate <NSObject>
- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id;
@end

@interface ImageViewCell : WaterFlowViewCell
{
    UIImageView *imageView;
    int WB_ID;
}
@property (nonatomic, assign) id <ImageViewCellDelegate> delegate;
-(void)setImageWithURL:(NSURL *)imageUrl withWB_ID:(int)wb_id withDelegate:(id)Delegate;
-(void)setImage:(UIImage *)image withWB_ID:(int)wb_id;
-(void)relayoutViews;

@end
