//
//  ViewController.h
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface ViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    NSMutableArray *arrayImg;
    WaterFlowView  *waterFlow;
    int selected_cell;
    int selected_cell_index;
    UIImage *selected_img;
}

- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end
