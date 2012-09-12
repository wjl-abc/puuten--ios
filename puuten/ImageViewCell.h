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
          clickedCell:(int)cell_id
           clickedImg:(UIImage *)img;

- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id
         clickerOrder:(int)cell_order
           clickedImg:(UIImage *)img;

- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id;

@end

@interface ImageViewCell : WaterFlowViewCell
{
    UIImageView *imageView;
    UILabel *bsName;
    int type;
    UIImageView *avatar;
    UILabel *name;
    NSString *partnerName;
    UILabel *info;
    int WB_ID;
    int order;
}
@property (assign, nonatomic) int tt;
@property (nonatomic, assign) id <ImageViewCellDelegate> delegate;
-(void)setImageWithURL:(NSURL *)imageUrl
             withWB_ID:(int)wb_id
                withBS:(NSString *)BSinfo
              withType:(int)Type
          withDelegate:(id)Delegate;

-(void)setImageWithURL:(NSURL *)imageUrl
             withWB_ID:(int)wb_id
                withBS:(NSString *)BSinfo
              withType:(int)Type
            withAvatar:(NSURL *)avatarUrl
              withName:(NSString *)Name
              withInfo:(NSString *)Info
          withDelegate:(id)Delegate;

-(void)setImageWithURL:(NSURL *)imageUrl
             withWB_ID:(int)wb_id
             withOrder:(int)Order
                withBS:(NSString *)BSinfo
              withType:(int)Type
            withAvatar:(NSURL *)avatarUrl
              withName:(NSString *)Name
              withInfo:(NSString *)Info
          withDelegate:(id)Delegate;

-(void)setImageWithImg:(UIImage *)image
             withWB_ID:(int)wb_id
                withBS:(NSString *)BSinfo
              withType:(int)Type
          withDelegate:(id)Delegate;

-(void)setImageWithImg:(UIImage *)image
             withWB_ID:(int)wb_id
                withBS:(NSString *)BSinfo
              withType:(int)Type
            withAvatar:(NSURL *)avatarUrl
              withName:(NSString *)Name
              withInfo:(NSString *)Info
          withDelegate:(id)Delegate;

-(void)setImageWithImg:(UIImage *)image
             withWB_ID:(int)wb_id
             withOrder:(int)Order
                withBS:(NSString *)BSinfo
              withType:(int)Type
            withAvatar:(NSURL *)avatarUrl
              withName:(NSString *)Name
              withInfo:(NSString *)Info
          withDelegate:(id)Delegate;

-(void)setImage:(UIImage *)image withWB_ID:(int)wb_id withBS:(NSString *)BSinfo;
-(void)relayoutViews;

@end
