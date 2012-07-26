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

@interface ViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    WaterFlowView  *waterFlow;
    int selected_cell;
}

- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end
